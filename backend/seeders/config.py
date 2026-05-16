import os


RANDOM_SEED = 20260516

DEFAULT_MAHASISWA_COUNT = 180
DEFAULT_PARKING_LOGS = 900
DEFAULT_ACCESS_REQUESTS = 5
MAX_ACCESS_REQUESTS = 5
DEFAULT_PENDING_STNK = 60
DEFAULT_LOG_DAYS = 21

PRODI_NAMES = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Elektro",
    "Teknik Sipil",
    "Arsitektur",
    "Manajemen",
    "Akuntansi",
    "Ilmu Komunikasi",
    "Pendidikan Matematika",
    "Desain Komunikasi Visual",
]

FIRST_NAMES = [
    "Ahmad",
    "Aulia",
    "Bagas",
    "Citra",
    "Dewi",
    "Dimas",
    "Eka",
    "Fajar",
    "Fitri",
    "Gilang",
    "Hana",
    "Ilham",
    "Intan",
    "Joko",
    "Kartika",
    "Laras",
    "Maya",
    "Naufal",
    "Putri",
    "Rizky",
    "Salsa",
    "Taufik",
    "Vina",
    "Wahyu",
    "Yusuf",
]

LAST_NAMES = [
    "Pratama",
    "Saputra",
    "Lestari",
    "Wibowo",
    "Rahmawati",
    "Maulana",
    "Kurniawan",
    "Permatasari",
    "Hidayat",
    "Nugroho",
    "Puspitasari",
    "Wijaya",
    "Ramadhan",
    "Utami",
    "Setiawan",
    "Anggraini",
]

MOTOR_BRANDS = [
    "Honda Beat",
    "Honda Vario 160",
    "Yamaha NMAX",
    "Yamaha Aerox",
    "Suzuki Nex II",
    "Honda Scoopy",
    "Yamaha Mio",
]

CAR_BRANDS = [
    "Toyota Avanza",
    "Honda Brio",
    "Daihatsu Sigra",
    "Toyota Agya",
    "Suzuki Ertiga",
    "Mitsubishi Xpander",
]

FLAG_REASONS = [
    "Sering parkir di luar area yang ditentukan",
    "Pernah meminjamkan kartu RFID ke orang lain",
    "Belum menyelesaikan teguran parkir sebelumnya",
    "Kendaraan beberapa kali tidak sesuai data",
]


def int_env(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default
