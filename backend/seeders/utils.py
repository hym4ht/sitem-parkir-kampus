import os

import models

from .config import FIRST_NAMES, LAST_NAMES


def get_or_create_prodi(db, name):
    prodi = db.query(models.Prodi).filter(models.Prodi.nama == name).first()
    if prodi:
        return prodi

    prodi = models.Prodi(nama=name)
    db.add(prodi)
    db.flush()
    return prodi


def get_or_create_user(db, nim_npp, **payload):
    user = db.query(models.User).filter(models.User.nim_npp == nim_npp).first()
    if user:
        return user

    user = models.User(nim_npp=nim_npp, **payload)
    db.add(user)
    db.flush()
    return user


def get_stnk_paths():
    backend_dir = os.path.dirname(os.path.dirname(__file__))
    upload_dir = os.path.join(backend_dir, "uploads", "stnk")
    if not os.path.isdir(upload_dir):
        return []

    paths = []
    for filename in sorted(os.listdir(upload_dir)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            paths.append(f"/uploads/stnk/{filename}")
    return paths


def make_student_name(index):
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index * 3) % len(LAST_NAMES)]
    if index % 4 == 0:
        middle = FIRST_NAMES[(index * 5) % len(FIRST_NAMES)]
        return f"{first} {middle} {last}"
    return f"{first} {last}"


def make_plate(index):
    prefixes = ["G", "H", "B", "K", "D", "AB", "AD", "E", "F", "L"]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    prefix = prefixes[index % len(prefixes)]
    number = 1000 + ((index * 37) % 8000)
    suffix = f"{letters[(index * 7) % 26]}{letters[(index * 11) % 26]}"
    return f"{prefix} {number} {suffix}"


def approved_vehicles(db):
    return (
        db.query(models.Vehicle)
        .join(models.User, models.Vehicle.user_id == models.User.id)
        .filter(
            models.User.role == models.RoleEnum.mahasiswa,
            models.Vehicle.status_validasi == models.ValidationStatusEnum.disetujui,
        )
        .all()
    )
