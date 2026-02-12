# Generated migration to fix Employee to User transition
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_employee_user_alter_task_assigned_to'),
    ]

    operations = [
        # Drop the old many-to-many table if it exists
        migrations.RunSQL(
            sql="""
                DROP TABLE IF EXISTS tasks_task_assigned_to CASCADE;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),

        # Create the new many-to-many table with correct structure
        migrations.RunSQL(
            sql="""
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

                CREATE INDEX IF NOT EXISTS tasks_task_assigned_to_task_id_idx
                    ON tasks_task_assigned_to(task_id);
                CREATE INDEX IF NOT EXISTS tasks_task_assigned_to_user_id_idx
                    ON tasks_task_assigned_to(user_id);
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS tasks_task_assigned_to CASCADE;
            """
        ),
    ]
