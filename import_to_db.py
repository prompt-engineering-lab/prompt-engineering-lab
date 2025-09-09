import sqlite3
import csv
import os
# Path to GTFS folder and database
GTFS_FOLDER = "group-task-skeleton/OtwartyWroclaw_rozklad_jazdy_GTFS"
DB_PATH = "trips.sqlite"

def create_table_from_csv(cursor, table_name, csv_path):
    with open(csv_path, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        columns = ', '.join([f'"{h}" TEXT' for h in headers])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')


def insert_csv_to_table(cursor, table_name, csv_path):
    with open(csv_path, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        placeholders = ', '.join(['?' for _ in headers])
        for row in reader:
            cursor.execute(f'INSERT INTO "{table_name}" VALUES ({placeholders})', row)


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for filename in os.listdir(GTFS_FOLDER):
        print(filename)
        if filename.endswith('.txt'):
            table_name = filename.replace('.txt', '')
            csv_path = os.path.join(GTFS_FOLDER, filename)
            print(f'Processing {filename}...')
            create_table_from_csv(cursor, table_name, csv_path)
            cursor.execute(f'DELETE FROM "{table_name}"')  # SQLite doesn't support TRUNCATE
            insert_csv_to_table(cursor, table_name, csv_path)
    conn.commit()
    conn.close()
    print('All GTFS files imported successfully.')

if __name__ == "__main__":
    main()
