"""Back up stayready.db to timestamped snapshots, pruning old ones.

Protects against app bugs, bad migrations, and accidental deletes — NOT
against losing the whole host (these backups live on the same disk as the
live database). Once deployed, also copy backups/ off-host on whatever
schedule the hosting platform supports (e.g. a periodic job pushing to
object storage) — that wiring is host-specific and deliberately not done
here since no hosting platform has been chosen yet.

Usage: python backup_db.py [--keep N]   (default keep: 14)
Schedule it (cron on Linux hosts, Task Scheduler on Windows) to run daily.
"""
import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from db import DATA_DIR

DATA_DIR = Path(DATA_DIR)
DB_PATH = DATA_DIR / 'stayready.db'
BACKUP_DIR = DATA_DIR / 'backups'


def backup(keep=14):
    if not DB_PATH.exists():
        print(f'No database at {DB_PATH} yet — nothing to back up.')
        return

    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = BACKUP_DIR / f'stayready-{stamp}.db'
    # sqlite3's backup API copies a consistent snapshot even if the app is
    # writing concurrently; a plain file copy could grab a mid-write state.
    src_conn = sqlite3.connect(DB_PATH)
    dest_conn = sqlite3.connect(dest)
    with dest_conn:
        src_conn.backup(dest_conn)
    src_conn.close()
    dest_conn.close()
    print(f'Backed up to {dest}')

    snapshots = sorted(BACKUP_DIR.glob('stayready-*.db'))
    stale = snapshots[:-keep] if keep > 0 else snapshots
    for old in stale:
        old.unlink()
        print(f'Pruned {old.name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--keep', type=int, default=14,
                        help='how many recent snapshots to retain (default 14)')
    args = parser.parse_args()
    try:
        backup(args.keep)
    except Exception as err:
        print(f'Backup failed: {err}', file=sys.stderr)
        sys.exit(1)
