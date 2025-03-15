import sqlite3
import bcrypt
import os

# Path to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'development.db'))
print(f"Connecting to database: {db_path}")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Display the current hash
cursor.execute("SELECT password FROM users WHERE email = 'admin@hbnb.io'")
result = cursor.fetchone()

if not result:
    print("Administrator not found!")
    conn.close()
    exit(1)

current_hash = result[0]
print(f"Current hash: {current_hash}")

# Generate a new hash for 'admin1234'
password = 'admin1234'
salt = bcrypt.gensalt()
new_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(f"New hash: {new_hash}")

# Update the password
cursor.execute("UPDATE users SET password = ? WHERE email = 'admin@hbnb.io'", (new_hash,))
conn.commit()
print("Password updated successfully!")

# Verify the update
cursor.execute("SELECT password FROM users WHERE email = 'admin@hbnb.io'")
updated_hash = cursor.fetchone()[0]
print(f"Updated hash: {updated_hash}")

# Close the connection
conn.close()