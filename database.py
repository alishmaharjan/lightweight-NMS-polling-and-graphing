import sqlite3
from datetime import datetime

DB = "traffic.db"


def connect():
    return sqlite3.connect(DB)


def init_db():

    conn = connect()
    cur = conn.cursor()

    # Raw SNMP Counters
    cur.execute("""
    CREATE TABLE IF NOT EXISTS traffic(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        interface TEXT,
        rx_bytes INTEGER,
        tx_bytes INTEGER
    )
    """)

    # Calculated Rates
    cur.execute("""
    CREATE TABLE IF NOT EXISTS traffic_rates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        interface TEXT,

        rx_mbps REAL,
        tx_mbps REAL,

        rx_util REAL,
        tx_util REAL,
	status TEXT,
	speed INTEGER
    )
    """)

    # Interface Information
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interfaces(
        interface TEXT PRIMARY KEY,

        ifindex INTEGER,

        speed_mbps INTEGER,

        admin_status INTEGER,

        oper_status INTEGER,

        last_seen TEXT
    )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------------

def insert_counter(interface, rx, tx):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO traffic(
            timestamp,
            interface,
            rx_bytes,
            tx_bytes
        )
        VALUES(?,?,?,?)
    """,
    (
        datetime.now().isoformat(),
        interface,
        rx,
        tx
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------------

def get_last_counter(interface):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            rx_bytes,
            tx_bytes,
            timestamp

        FROM traffic

        WHERE interface=?

        ORDER BY id DESC

        LIMIT 1
    """,(interface,))

    row = cur.fetchone()

    conn.close()

    return row


# --------------------------------------------------------

def insert_rate(interface, rx_mbps, tx_mbps,
                rx_util, tx_util, status, speed):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO traffic_rates(
            timestamp,
            interface,

            rx_mbps,
            tx_mbps,

            rx_util,
            tx_util,

	    status,
	    speed
        )

        VALUES(?,?,?,?,?,?,?,?)
    """,
    (
        datetime.now().isoformat(),
        interface,

        rx_mbps,
        tx_mbps,

        rx_util,
        tx_util,
	status,
	speed

    ))

    conn.commit()
    conn.close()


# --------------------------------------------------------

def update_interface(

        interface,
        ifindex,

        speed,

        admin,

        oper
):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

        INSERT OR REPLACE INTO interfaces(

            interface,

            ifindex,

            speed_mbps,

            admin_status,

            oper_status,

            last_seen

        )

        VALUES(

            ?,?,?,?,?,?

        )

    """,
    (

        interface,

        ifindex,

        speed,

        admin,

        oper,

        datetime.now().isoformat()

    ))

    conn.commit()
    conn.close()


# --------------------------------------------------------

def latest_rates():

    conn = connect()

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM traffic_rates

        WHERE id IN(

            SELECT MAX(id)

            FROM traffic_rates

            GROUP BY interface

        )

        ORDER BY interface

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


if __name__ == "__main__":

    init_db()

    print("Database Ready")
