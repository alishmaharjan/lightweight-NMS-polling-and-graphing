from flask import Flask, jsonify, render_template
import sqlite3

DB = "traffic.db"

app = Flask(__name__)


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/interfaces")
def interfaces():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM traffic_rates

        WHERE id IN (

            SELECT MAX(id)

            FROM traffic_rates

            GROUP BY interface

        )

        ORDER BY interface

    """)

    rows = cur.fetchall()
    conn.close()

    data = []

    total_rx = 0
    total_tx = 0

    up = 0
    down = 0

    for row in rows:

        total_rx += row["rx_mbps"]
        total_tx += row["tx_mbps"]

        if row["status"] == "UP":
            up += 1
        else:
            down += 1

        data.append({

            "interface": row["interface"],

            "status": row["status"],

            "speed": row["speed"],

            "rx_mbps": round(row["rx_mbps"], 2),

            "tx_mbps": round(row["tx_mbps"], 2),

            "rx_util": round(row["rx_util"], 2),

            "tx_util": round(row["tx_util"], 2)

        })

    return jsonify({

        "summary": {

            "total_ports": len(data),

            "ports_up": up,

            "ports_down": down,

            "total_rx": round(total_rx, 2),

            "total_tx": round(total_tx, 2)

        },

        "interfaces": data

    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
