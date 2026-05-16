import argparse

from seeders.config import (
    DEFAULT_ACCESS_REQUESTS,
    DEFAULT_LOG_DAYS,
    DEFAULT_MAHASISWA_COUNT,
    DEFAULT_PARKING_LOGS,
    DEFAULT_PENDING_STNK,
    MAX_ACCESS_REQUESTS,
    int_env,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Seed demo data for Smart Campus Parking System."
    )
    parser.add_argument(
        "--mahasiswa",
        type=int,
        default=int_env("SEED_MAHASISWA", DEFAULT_MAHASISWA_COUNT),
        help="Jumlah mahasiswa demo yang ditargetkan.",
    )
    parser.add_argument(
        "--logs",
        type=int,
        default=int_env("SEED_PARKING_LOGS", DEFAULT_PARKING_LOGS),
        help="Jumlah total log keluar/masuk parkir yang ditargetkan.",
    )
    parser.add_argument(
        "--access-requests",
        type=int,
        default=int_env("SEED_ACCESS_REQUESTS", DEFAULT_ACCESS_REQUESTS),
        help=f"Jumlah total permintaan gerbang yang ditargetkan, maksimal {MAX_ACCESS_REQUESTS}.",
    )
    parser.add_argument(
        "--pending-stnk",
        type=int,
        default=int_env("SEED_PENDING_STNK", DEFAULT_PENDING_STNK),
        help="Jumlah kendaraan demo yang dibuat sebagai pending STNK.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=int_env("SEED_LOG_DAYS", DEFAULT_LOG_DAYS),
        help="Sebaran hari ke belakang untuk log parkir.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    from seeders.runner import seed_data

    seed_data(
        mahasiswa_count=max(args.mahasiswa, 0),
        parking_logs=max(args.logs, 0),
        access_requests=min(max(args.access_requests, 0), MAX_ACCESS_REQUESTS),
        pending_stnk=max(args.pending_stnk, 0),
        log_days=max(args.days, 1),
    )
