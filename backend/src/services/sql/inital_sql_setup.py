import sqlite3

# Connect to the database
conn = sqlite3.connect('../../../zahav.db')
cursor = conn.cursor()

# Create main table
cursor.execute('''CREATE TABLE calc_results (
                        id INTEGER PRIMARY KEY,
                        payload_mass FLOAT,
                        takeoff_distance FLOAT,
                        excess_payload_mass FLOAT,
                        takeoff_time FLOAT
                    );
                ''')


conn.commit()
conn.close()
