# Database Migration Fix - README

## Problem
Error: `column tasks_task_assigned_to.user_id does not exist`

This happens because the Task model changed from Employee to User but the database still has the old structure.

## Solution Options (Pick ONE)

### Option 1: Quick Fix (EASIEST) ⭐
Just double-click this file:
```
quick_fix.bat
```

### Option 2: Direct Python Fix
Run this command:
```bash
task_env\Scripts\activate
python fix_db_direct.py
```

### Option 3: Manual Commands
```bash
# Activate virtual environment
task_env\Scripts\activate

# Run migration
python manage.py migrate

# If error persists:
python manage.py migrate tasks 0006_fix_assigned_to_table --fake

# Then run again:
python manage.py migrate
```

### Option 4: Fresh Start (Development Only - WILL DELETE DATA)
```bash
task_env\Scripts\activate
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## After Fix
1. Run server: `python manage.py runserver`
2. Go to: http://127.0.0.1:8000/admin
3. Create Users and assign them to Groups (Manager/Employee)
4. Create Tasks and assign Users to them

## What Was Fixed
- Changed `assigned_to` from Employee model to User model
- Updated all templates to use User fields (username, first_name, email)
- Updated all views to filter by User instead of Employee
- Added task detail page with:
  - Title, Description, Priority, Status
  - Date/Time information
  - Team members list
  - Status change functionality
  - Edit/Delete buttons

## Files Changed
1. `tasks/models.py` - Task.assigned_to → User
2. `tasks/views.py` - All Employee references → User
3. `tasks/templates/task_detail.html` - Complete redesign
4. `tasks/templates/dashboard/*.html` - User fields
5. `tasks/migrations/0006_fix_assigned_to_table.py` - New migration

## Need Help?
Run: `python manage.py showmigrations tasks`

This shows which migrations are applied.
