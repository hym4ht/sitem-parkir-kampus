import random
from datetime import datetime, timedelta, timezone

import models

from .config import RANDOM_SEED
from .utils import approved_vehicles


def seed_parking_logs(db, target_logs, days):
    current_logs = db.query(models.ParkingLog).count()
    if current_logs >= target_logs:
        return 0

    vehicles = approved_vehicles(db)
    if not vehicles:
        return 0

    rng = random.Random(RANDOM_SEED + current_logs)
    now = datetime.now(timezone.utc)
    to_create = target_logs - current_logs
    created = 0

    while created < to_create:
        vehicle = vehicles[(current_logs + created) % len(vehicles)]
        day_offset = rng.randint(0, max(days - 1, 0))

        if day_offset == 0:
            start_hour = rng.randint(6, max(now.hour, 7))
            start_minute = rng.randint(0, 59)
            masuk_time = now.replace(
                hour=min(start_hour, 23),
                minute=start_minute,
                second=rng.randint(0, 59),
                microsecond=0,
            )
            if masuk_time > now:
                masuk_time = now - timedelta(minutes=rng.randint(1, 90))
        else:
            masuk_time = (now - timedelta(days=day_offset)).replace(
                hour=rng.randint(6, 18),
                minute=rng.randint(0, 59),
                second=rng.randint(0, 59),
                microsecond=0,
            )

        status_akses = (
            models.AccessStatusEnum.manual_petugas
            if rng.random() < 0.18
            else models.AccessStatusEnum.otomatis
        )

        db.add(
            models.ParkingLog(
                user_id=vehicle.user_id,
                vehicle_id=vehicle.id,
                waktu=masuk_time,
                jenis_aktivitas=models.ActivityTypeEnum.masuk,
                status_akses=status_akses,
            )
        )
        created += 1

        should_add_exit = created < to_create and rng.random() > 0.12
        if should_add_exit:
            candidate_keluar_time = masuk_time + timedelta(
                hours=rng.randint(1, 9),
                minutes=rng.randint(5, 55),
            )
            if candidate_keluar_time > now:
                minutes_until_now = int((now - masuk_time).total_seconds() // 60)
                if minutes_until_now < 5:
                    keluar_time = None
                else:
                    keluar_time = masuk_time + timedelta(
                        minutes=rng.randint(5, minutes_until_now)
                    )
            else:
                keluar_time = candidate_keluar_time

            if keluar_time:
                db.add(
                    models.ParkingLog(
                        user_id=vehicle.user_id,
                        vehicle_id=vehicle.id,
                        waktu=keluar_time,
                        jenis_aktivitas=models.ActivityTypeEnum.keluar,
                        status_akses=status_akses,
                    )
                )
                created += 1

        if created % 200 == 0:
            db.commit()

    db.commit()
    return created
