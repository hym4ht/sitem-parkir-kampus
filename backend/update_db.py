from sqlalchemy import create_engine, text
from core.config import settings

def update_database():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        print("Checking for existing columns in 'users' table...")
        
        # Add is_flagged if it doesn't exist
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_flagged INTEGER DEFAULT 0"))
            print("Added 'is_flagged' column to users.")
        except Exception as e:
            print(f"Column 'is_flagged' might already exist: {e}")

        # Add flag_reason if it doesn't exist
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN flag_reason VARCHAR(255)"))
            print("Added 'flag_reason' column to users.")
        except Exception as e:
            print(f"Column 'flag_reason' might already exist: {e}")

        print("Updating 'announcements' table...")
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS announcements (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    message VARCHAR(500) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NULL,
                    sender_id INTEGER NOT NULL,
                    FOREIGN KEY (sender_id) REFERENCES users(id)
                )
            """))
            # In case table exists but column doesn't
            try:
                conn.execute(text("ALTER TABLE announcements ADD COLUMN expires_at DATETIME NULL"))
                print("Added 'expires_at' column to announcements.")
            except:
                pass
            print("Table 'announcements' updated.")
        except Exception as e:
            print(f"Error updating announcements table: {e}")
        
        conn.commit()

if __name__ == "__main__":
    update_database()
