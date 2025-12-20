import csv 
import mysql.connector 
from database.config import DB_CONFIG

conn = mysql.connector.connect(** DB_CONFIG)

insert_sql = """
INSERT INTO laravel_devs (github_username, email)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE email = VALUES(email);
"""

with conn.cursor() as cursor:
    with open("laravel_devs.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            github_username = row["github_username"].strip()
            email = row["email"].strip()

            
            if not email:
                continue

            cursor.execute(insert_sql, (github_username, email))

    conn.commit()

conn.close()

print("CSV data imported successfully ")