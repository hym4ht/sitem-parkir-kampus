import socket
import traceback

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url

from core.config import settings


def sanitize_database_url(raw_url: str) -> str:
    url = make_url(raw_url)
    return url.render_as_string(hide_password=True)


def main():
    raw_url = settings.DATABASE_URL
    url = make_url(raw_url)
    host = url.host or "localhost"
    port = url.port or 3306

    print("== Smart Parking DB Debug ==")
    print(f"DATABASE_URL: {sanitize_database_url(raw_url)}")
    print(f"Driver: {url.drivername}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {url.database}")
    print()

    try:
        addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        resolved = sorted({item[4][0] for item in addresses})
        print(f"[OK] DNS/host resolved: {', '.join(resolved)}")
    except Exception:
        print("[FAIL] DNS/host tidak bisa resolve")
        traceback.print_exc()
        return

    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"[OK] TCP connect ke {host}:{port}")
    except Exception:
        print(f"[FAIL] TCP connect ke {host}:{port} gagal")
        traceback.print_exc()
        return

    try:
        engine = create_engine(raw_url, pool_pre_ping=True)
        with engine.connect() as conn:
            mysql_version = conn.execute(text("SELECT VERSION()")).scalar()
            selected_db = conn.execute(text("SELECT DATABASE()")).scalar()
            print(f"[OK] MySQL connected: {mysql_version}")
            print(f"[OK] Selected database: {selected_db}")

            tables = inspect(conn).get_table_names()
            print(f"[OK] Tables ({len(tables)}): {', '.join(tables) if tables else '-'}")

            if "users" in tables:
                user_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
                print(f"[OK] users count: {user_count}")

                seed_users = conn.execute(
                    text(
                        "SELECT nim_npp, role FROM users "
                        "WHERE nim_npp IN ('admin123', 'petugas123', '11223344', '55667788') "
                        "ORDER BY nim_npp"
                    )
                ).fetchall()
                if seed_users:
                    print("[OK] Seed users:")
                    for nim_npp, role in seed_users:
                        print(f"  - {nim_npp} / {role}")
                else:
                    print("[WARN] Seed users belum ada. Jalankan: python seed.py")
            else:
                print("[FAIL] Table users belum ada. Pastikan migrasi/create_all sudah jalan.")
    except Exception:
        print("[FAIL] SQLAlchemy/MySQL query gagal")
        traceback.print_exc()
        return

    print()
    print("[DONE] Database backend bisa diakses.")


if __name__ == "__main__":
    main()
