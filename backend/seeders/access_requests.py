import random
from datetime import datetime, timedelta, timezone

import models

from .config import MAX_ACCESS_REQUESTS, RANDOM_SEED
from .utils import approved_vehicles


def seed_access_requests(db, target_requests):
    target_requests = min(target_requests, MAX_ACCESS_REQUESTS)
    current_requests = db.query(models.AccessRequest).count()
    if current_requests >= target_requests:
        return 0

    vehicles = approved_vehicles(db)
    if not vehicles:
        return 0

    existing_pending_user_ids = {
        row[0]
        for row in db.query(models.AccessRequest.user_id)
        .filter(models.AccessRequest.status == models.AccessRequestStatusEnum.pending)
        .all()
    }

    rng = random.Random(RANDOM_SEED + current_requests + 99)
    now = datetime.now(timezone.utc)
    to_create = target_requests - current_requests
    created = 0

    pending_quota = min(int(to_create * 0.65), len(vehicles))
    for vehicle in vehicles:
        if created >= pending_quota:
            break
        if vehicle.user_id in existing_pending_user_ids:
            continue

        db.add(
            models.AccessRequest(
                user_id=vehicle.user_id,
                vehicle_id=vehicle.id,
                jenis_aktivitas=(
                    models.ActivityTypeEnum.masuk
                    if created % 2 == 0
                    else models.ActivityTypeEnum.keluar
                ),
                status=models.AccessRequestStatusEnum.pending,
                waktu_request=now - timedelta(
                    minutes=rng.randint(0, 4),
                    seconds=rng.randint(0, 59),
                ),
            )
        )
        existing_pending_user_ids.add(vehicle.user_id)
        created += 1

    while created < to_create:
        vehicle = vehicles[(current_requests + created) % len(vehicles)]
        request_time = now - timedelta(
            days=rng.randint(0, 10),
            hours=rng.randint(1, 18),
            minutes=rng.randint(0, 59),
        )
        approved = rng.random() > 0.28
        status = (
            models.AccessRequestStatusEnum.disetujui
            if approved
            else models.AccessRequestStatusEnum.ditolak
        )

        db.add(
            models.AccessRequest(
                user_id=vehicle.user_id,
                vehicle_id=vehicle.id,
                jenis_aktivitas=(
                    models.ActivityTypeEnum.masuk
                    if rng.random() > 0.45
                    else models.ActivityTypeEnum.keluar
                ),
                status=status,
                waktu_request=request_time,
                waktu_respon=request_time + timedelta(minutes=rng.randint(1, 9)),
                catatan=(
                    None
                    if approved
                    else "Data akses perlu diverifikasi ulang oleh petugas"
                ),
            )
        )
        created += 1

        if created % 200 == 0:
            db.commit()

    db.commit()
    return created
