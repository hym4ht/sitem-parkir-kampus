from database import Base, SessionLocal, engine
import models

from .access_requests import seed_access_requests
from .core import seed_core_data
from .parking import seed_parking_logs
from .students import seed_demo_students


def seed_data(mahasiswa_count, parking_logs, access_requests, pending_stnk, log_days):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        prodi_by_name = seed_core_data(db)
        seed_demo_students(
            db,
            prodi_by_name,
            mahasiswa_count=mahasiswa_count,
            pending_stnk_count=pending_stnk,
        )
        created_logs = seed_parking_logs(db, target_logs=parking_logs, days=log_days)
        created_requests = seed_access_requests(db, target_requests=access_requests)

        total_mahasiswa = (
            db.query(models.User)
            .filter(models.User.role == models.RoleEnum.mahasiswa)
            .count()
        )
        total_vehicles = db.query(models.Vehicle).count()
        total_pending_stnk = (
            db.query(models.Vehicle)
            .filter(models.Vehicle.status_validasi == models.ValidationStatusEnum.pending)
            .count()
        )
        total_logs = db.query(models.ParkingLog).count()
        total_requests = db.query(models.AccessRequest).count()
        total_pending_requests = (
            db.query(models.AccessRequest)
            .filter(models.AccessRequest.status == models.AccessRequestStatusEnum.pending)
            .count()
        )

        print("[OK] Database seeded successfully.")
        print("Akun test:")
        print("  Admin:     admin123 / adminpassword")
        print("  Petugas:   petugas123 / petugaspassword")
        print("  Mahasiswa: 11223344 / mhspassword (flagged)")
        print("  Mahasiswa: 55667788 / mhspassword")
        print("Ringkasan data:")
        print(f"  Mahasiswa total:          {total_mahasiswa}")
        print(f"  Kendaraan total:          {total_vehicles}")
        print(f"  STNK pending total:       {total_pending_stnk}")
        print(f"  Log parkir total:         {total_logs} (+{created_logs})")
        print(f"  Request akses total:      {total_requests}")
        print(f"  Request akses pending:    {total_pending_requests}")
        print(f"  Request akses baru dibuat: {created_requests}")
    finally:
        db.close()
