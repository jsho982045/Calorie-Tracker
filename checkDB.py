import sqlite3

def check_entries():
    print("Connecting to database...")
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    print("Fetching entries...")
    c.execute('SELECT * FROM entries')
    entries = c.fetchall()
    if entries:
        print(f"Found {len(entries)} entries:")
        for entry in entries:
            print(entry)
    else:
        print("No entries found.")
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    check_entries()
