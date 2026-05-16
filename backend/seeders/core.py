import models
from core.security import get_password_hash

from .config import PRODI_NAMES
from .utils import get_or_create_prodi, get_or_create_user


def seed_core_data(db):
    prodi_by_name = {name: get_or_create_prodi(db, name) for name in PRODI_NAMES}
    db.commit()

    admin_password = get_password_hash("adminpassword")
    petugas_password = get_password_hash("petugaspassword")
    mahasiswa_password = get_password_hash("mhspassword")

    admin = get_or_create_user(
        db,
        "admin123",
        nama="Super Admin",
        role=models.RoleEnum.admin,
        password_hash=admin_password,
    )

    get_or_create_user(
        db,
        "petugas123",
        nama="Budi Petugas",
        role=models.RoleEnum.petugas,
        password_hash=petugas_password,
    )

    for idx, name in enumerate(["Rani Petugas", "Agus Petugas", "Sari Petugas"], 1):
        get_or_create_user(
            db,
            f"petugas{idx:03d}",
            nama=name,
            role=models.RoleEnum.petugas,
            password_hash=petugas_password,
        )

    mhs1 = get_or_create_user(
        db,
        "11223344",
        nama="Budi Santoso",
        prodi=prodi_by_name["Teknik Informatika"],
        angkatan=2023,
        rfid_uid="RFID_BUDI_123",
        role=models.RoleEnum.mahasiswa,
        password_hash=mahasiswa_password,
        is_flagged=1,
        flag_reason="Sering parkir di luar area yang ditentukan",
    )

    mhs2 = get_or_create_user(
        db,
        "55667788",
        nama="Siti Aminah",
        prodi=prodi_by_name["Sistem Informasi"],
        angkatan=2024,
        rfid_uid="RFID_SITI_456",
        role=models.RoleEnum.mahasiswa,
        password_hash=mahasiswa_password,
    )

    db.commit()

    seed_vehicle_if_missing(
        db,
        user=mhs1,
        plat_nomor="G 1234 AB",
        jenis_kendaraan=models.VehicleTypeEnum.motor,
        merek="Honda Vario 150",
        status_validasi=models.ValidationStatusEnum.disetujui,
    )
    seed_vehicle_if_missing(
        db,
        user=mhs2,
        plat_nomor="G 5678 CD",
        jenis_kendaraan=models.VehicleTypeEnum.motor,
        merek="Yamaha NMAX",
        status_validasi=models.ValidationStatusEnum.pending,
    )

    db.commit()
    seed_announcements(db, admin)
    return prodi_by_name


def seed_vehicle_if_missing(
    db,
    user,
    plat_nomor,
    jenis_kendaraan,
    merek,
    status_validasi,
    foto_stnk=None,
):
    vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.plat_nomor == plat_nomor)
        .first()
    )
    if vehicle:
        return vehicle

    vehicle = models.Vehicle(
        user_id=user.id,
        jenis_kendaraan=jenis_kendaraan,
        plat_nomor=plat_nomor,
        merek=merek,
        foto_stnk=foto_stnk,
        status_validasi=status_validasi,
    )
    db.add(vehicle)
    db.flush()
    return vehicle


def seed_announcements(db, admin_user):
    if db.query(models.Announcement).count() > 0:
        return

    messages = [
        "Mulai 1 Mei 2026, seluruh kendaraan wajib memiliki STNK yang terverifikasi untuk masuk area parkir kampus.",
        "Perbaikan jalur parkir motor gedung B akan dilakukan pada 3-5 Mei. Gunakan jalur alternatif.",
        "Petugas akan memprioritaskan permintaan akses manual untuk mahasiswa dengan kendaraan terdaftar.",
    ]
    for message in messages:
        db.add(models.Announcement(message=message, sender_id=admin_user.id))
    db.commit()
