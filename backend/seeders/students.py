import models
from core.security import get_password_hash

from .config import CAR_BRANDS, FLAG_REASONS, MOTOR_BRANDS
from .core import seed_vehicle_if_missing
from .utils import (
    get_or_create_user,
    get_stnk_paths,
    make_plate,
    make_student_name,
)


def seed_demo_students(db, prodi_by_name, mahasiswa_count, pending_stnk_count):
    password_hash = get_password_hash("mhspassword")
    stnk_paths = get_stnk_paths()
    prodi_list = list(prodi_by_name.values())
    students = []

    for index in range(1, mahasiswa_count + 1):
        nim = f"2026{index:05d}"
        prodi = prodi_list[index % len(prodi_list)]
        angkatan = 2021 + (index % 5)
        is_flagged = 1 if index % 17 == 0 else 0
        flag_reason = FLAG_REASONS[index % len(FLAG_REASONS)] if is_flagged else None

        user = get_or_create_user(
            db,
            nim,
            nama=make_student_name(index),
            prodi=prodi,
            angkatan=angkatan,
            rfid_uid=f"RFID_DEMO_{index:05d}",
            role=models.RoleEnum.mahasiswa,
            password_hash=password_hash,
            is_flagged=is_flagged,
            flag_reason=flag_reason,
        )
        students.append(user)

        if index <= pending_stnk_count:
            status = models.ValidationStatusEnum.pending
        elif index % 13 == 0:
            status = models.ValidationStatusEnum.ditolak
        else:
            status = models.ValidationStatusEnum.disetujui

        is_car = index % 9 == 0
        jenis = models.VehicleTypeEnum.mobil if is_car else models.VehicleTypeEnum.motor
        brands = CAR_BRANDS if is_car else MOTOR_BRANDS
        foto_stnk = stnk_paths[index % len(stnk_paths)] if stnk_paths else None

        seed_vehicle_if_missing(
            db,
            user=user,
            plat_nomor=make_plate(index),
            jenis_kendaraan=jenis,
            merek=brands[index % len(brands)],
            status_validasi=status,
            foto_stnk=foto_stnk,
        )

        if index % 50 == 0:
            db.commit()

    db.commit()
    return students
