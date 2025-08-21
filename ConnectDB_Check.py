# Insert sample data into all tables of CBS_Dev
import psycopg2

db_name = "WorkAtRisk_Dev"
print(f"\n--- Inserting data into {db_name} ---")
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database=db_name,
    user="your-postgres-username",
    password="your-postgres-password"
)
cur = conn.cursor()
conn.commit()

# # Truncate all tables and reset identity
# cur.execute('TRUNCATE TABLE "user_roles" RESTART IDENTITY CASCADE;')
# cur.execute('TRUNCATE TABLE "Role" RESTART IDENTITY CASCADE;')
# cur.execute('TRUNCATE TABLE "User" RESTART IDENTITY CASCADE;')

# Insert sample data into User table
cur.execute("""
INSERT INTO "User" (FirstName, LastName, MiddleName) VALUES
('John', 'Doe', 'A'),
('Jane', 'Smith', 'B'),
('Alice', 'Johnson', NULL)
RETURNING EmployeeId;
""")
user_ids = [row[0] for row in cur.fetchall()]

# Insert sample data into Role table
cur.execute("""
INSERT INTO "Role" (RoleName) VALUES
('Admin'),
('Manager'),
('Employee')
RETURNING RoleId;
""")
role_ids = [row[0] for row in cur.fetchall()]


# Insert sample data into User_Roles table using fetched IDs (if both user_ids and role_ids are available)
if user_ids and role_ids and len(user_ids) >= 3 and len(role_ids) >= 3:
    user_roles_data = [
        (user_ids[0], role_ids[0]),  # John - Admin
        (user_ids[0], role_ids[1]),  # John - Manager
        (user_ids[1], role_ids[1]),  # Jane - Manager
        (user_ids[2], role_ids[2])   # Alice - Employee
    ]
    cur.executemany('INSERT INTO user_roles (employeeid, roleid) VALUES (%s, %s);', user_roles_data)

conn.commit()

# Print all tables
cur.execute('SELECT * FROM "User";')
print('User table:', cur.fetchall())
cur.execute('SELECT * FROM "Role";')
print('Role table:', cur.fetchall())
cur.execute('SELECT * FROM user_roles;')
print('User_Roles table:', cur.fetchall())
print(f"Tables created and sample data inserted successfully in {db_name}!")
cur.close()
conn.close()