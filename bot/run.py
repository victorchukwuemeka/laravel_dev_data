import sys
print(sys.path)
import mysql.connector
from database.config import DB_CONFIG
from bot.mailer import send_email
import time

BATCH_SIZE = 10
conn = mysql.connector.connect(**DB_CONFIG)

select_sql = f"""
SELECT id, github_username, email
FROM laravel_devs
WHERE sent = 0 AND email IS NOT NULL
LIMIT {BATCH_SIZE};
"""

update_sql = """
UPDATE laravel_devs
SET sent = 1
WHERE id = %s;
"""

with conn.cursor(dictionary=True) as cursor:
    cursor.execute(select_sql)
    rows = cursor.fetchall()

    for row in rows:
        try:
            send_email(row["email"], row["github_username"])
            cursor.execute(update_sql, (row["id"],))
            conn.commit()
            print(f"Sent to {row['email']}")
            time.sleep(5)  

        except Exception as e:
            print(f"Failed for {row['email']}: {e}")

conn.close()
