import pymysql

try:
    # Connect directly to MySQL without selecting a database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306
    )
    
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS smart_parking_db")
    
    connection.commit()
    print("Database 'smart_parking_db' successfully created or already exists!")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
