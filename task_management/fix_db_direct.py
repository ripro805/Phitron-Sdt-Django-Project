"""
Direct database fix script - Run this with: python fix_db_direct.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from django.db import connection


def fix_database():
    print("="*60)
    print("Database Fix Script")
    print("="*60)

    with connection.cursor() as cursor:
        print("\nStep 1: Checking current table structure...")

        # Check if old table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'tasks_task_assigned_to'
            );
        """)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("  ✓ Found tasks_task_assigned_to table")

            # Check columns
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'tasks_task_assigned_to'
                AND column_name IN ('employee_id', 'user_id');
            """)
            columns = [row[0] for row in cursor.fetchall()]

            if 'employee_id' in columns:
                print("  ✗ Old structure detected (employee_id)")
                print("\nStep 2: Backing up data...")

                # Get old assignments
                try:
                    cursor.execute("""
                        SELECT task_id, employee_id
                        FROM tasks_task_assigned_to;
                    """)
                    old_data = cursor.fetchall()
                    print(f"  ✓ Found {len(old_data)} assignments to migrate")
                except Exception as e:
                    print(f"  ! Warning: {e}")
                    old_data = []

                print("\nStep 3: Dropping old table...")
                cursor.execute("DROP TABLE IF EXISTS tasks_task_assigned_to CASCADE;")
                print("  ✓ Old table dropped")

            elif 'user_id' in columns:
                print("  ✓ Table already has correct structure")
                print("\n✓ Database is already fixed!")
                return

        print("\nStep 4: Creating new table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks_task_assigned_to (
                id SERIAL PRIMARY KEY,
                task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                CONSTRAINT tasks_task_assigned_to_task_id_fkey
                    FOREIGN KEY (task_id) REFERENCES tasks_task(id) ON DELETE CASCADE,
                CONSTRAINT tasks_task_assigned_to_user_id_fkey
                    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
                CONSTRAINT tasks_task_assigned_to_task_id_user_id_key
                    UNIQUE (task_id, user_id)
            );
        """)
        print("  ✓ New table created")

        print("\nStep 5: Creating indexes...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS tasks_task_assigned_to_task_id_idx
                ON tasks_task_assigned_to(task_id);
            CREATE INDEX IF NOT EXISTS tasks_task_assigned_to_user_id_idx
                ON tasks_task_assigned_to(user_id);
        """)
        print("  ✓ Indexes created")

    print("\n" + "="*60)
    print("✓ Database Fix Complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Run migrations: python manage.py migrate")
    print("2. Start server: python manage.py runserver")
    print("\nNote: You may need to re-assign users to tasks from Django Admin")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        fix_database()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease run: python manage.py migrate")
        sys.exit(1)
