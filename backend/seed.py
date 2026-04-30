from database import SessionLocal, engine, Base
import models
from core.security import get_password_hash

# Note: ensure database tables exist (already done by main.py)
db = SessionLocal()

def seed_data():
    # Prodi
    ti = db.query(models.Prodi).filter(models.Prodi.nama == "Teknik Informatika").first()
    if not ti:
        ti = models.Prodi(nama="Teknik Informatika")
        db.add(ti)
    
    si = db.query(models.Prodi).filter(models.Prodi.nama == "Sistem Informasi").first()
    if not si:
        si = models.Prodi(nama="Sistem Informasi")
        db.add(si)
    
    db.commit()
    db.refresh(ti)
    db.refresh(si)

    # Admin
    if not db.query(models.User).filter(models.User.nim_npp == "admin123").first():
        admin = models.User(
            nim_npp="admin123",
            nama="Super Admin",
            role=models.RoleEnum.admin,
            password_hash=get_password_hash("adminpassword")
        )
        db.add(admin)

    # Petugas
    if not db.query(models.User).filter(models.User.nim_npp == "petugas123").first():
        petugas = models.User(
            nim_npp="petugas123",
            nama="Budi Petugas",
            role=models.RoleEnum.petugas,
            password_hash=get_password_hash("petugaspassword")
        )
        db.add(petugas)

    # Mahasiswa 1 (flagged)
    mhs1 = db.query(models.User).filter(models.User.nim_npp == "11223344").first()
    if not mhs1:
        mhs1 = models.User(
            nim_npp="11223344",
            nama="Budi Santoso",
            prodi=ti,
            angkatan=2023,
            rfid_uid="RFID_BUDI_123",
            role=models.RoleEnum.mahasiswa,
            password_hash=get_password_hash("mhspassword"),
            is_flagged=1,
            flag_reason="Sering parkir di luar area yang ditentukan"
        )
        db.add(mhs1)

    # Mahasiswa 2 (clean)
    mhs2 = db.query(models.User).filter(models.User.nim_npp == "55667788").first()
    if not mhs2:
        mhs2 = models.User(
            nim_npp="55667788",
            nama="Siti Aminah",
            prodi=si,
            angkatan=2024,
            rfid_uid="RFID_SITI_456",
            role=models.RoleEnum.mahasiswa,
            password_hash=get_password_hash("mhspassword")
        )
        db.add(mhs2)
    
    db.commit()

    # Vehicles
    if mhs1 and not db.query(models.Vehicle).filter(models.Vehicle.plat_nomor == "G 1234 AB").first():
        v1 = models.Vehicle(
            user_id=mhs1.id,
            jenis_kendaraan=models.VehicleTypeEnum.motor,
            plat_nomor="G 1234 AB",
            merek="Honda Vario 150",
            status_validasi=models.ValidationStatusEnum.disetujui
        )
        db.add(v1)

    if mhs2 and not db.query(models.Vehicle).filter(models.Vehicle.plat_nomor == "G 5678 CD").first():
        v2 = models.Vehicle(
            user_id=mhs2.id,
            jenis_kendaraan=models.VehicleTypeEnum.motor,
            plat_nomor="G 5678 CD",
            merek="Yamaha NMAX",
            status_validasi=models.ValidationStatusEnum.pending
        )
        db.add(v2)

    db.commit()

    # Announcements
    admin_user = db.query(models.User).filter(models.User.nim_npp == "admin123").first()
    if admin_user and db.query(models.Announcement).count() == 0:
        ann1 = models.Announcement(
            message="Mulai 1 Mei 2026, seluruh kendaraan wajib memiliki STNK yang terverifikasi untuk masuk area parkir kampus.",
            sender_id=admin_user.id
        )
        ann2 = models.Announcement(
            message="Perbaikan jalur parkir motor gedung B akan dilakukan pada 3-5 Mei. Gunakan jalur alternatif.",
            sender_id=admin_user.id
        )
        db.add(ann1)
        db.add(ann2)
        db.commit()

    print("[OK] Database seeded with test data successfully!")
    print("   Akun Test:")
    print("   - Admin:     admin123 / adminpassword")
    print("   - Petugas:   petugas123 / petugaspassword")
    print("   - Mahasiswa: 11223344 / mhspassword (FLAGGED)")
    print("   - Mahasiswa: 55667788 / mhspassword (Clean)")

if __name__ == "__main__":
    seed_data()
