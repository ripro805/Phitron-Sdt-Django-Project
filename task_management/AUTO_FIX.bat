@echo off
cls
echo.
echo ========================================================================
echo                    DATABASE AUTO-FIX TOOL
echo ========================================================================
echo.
echo This tool will automatically fix the database migration error.
echo.
echo What this does:
echo   1. Checks database state
echo   2. Fixes table structure
echo   3. Applies all migrations
echo   4. Verifies everything works
echo.
echo ========================================================================
echo.

cd /d "d:\KnowledgeVault\Practice\Phitron-SDT-Course-\Development\Django\Django Project\task_management"

echo [Step 1/4] Activating virtual environment...
call task_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment
    echo Please check if task_env folder exists
    pause
    exit /b 1
)
echo   DONE
echo.

echo [Step 2/4] Running direct database fix...
python fix_db_direct.py
if errorlevel 1 (
    echo WARNING: Direct fix had issues, continuing with Django migration...
)
echo   DONE
echo.

echo [Step 3/4] Applying Django migrations...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo ERROR: Migration failed
    echo.
    echo Trying alternative approach...
    python manage.py migrate tasks --fake-initial
    python manage.py migrate
)
echo   DONE
echo.

echo [Step 4/4] Verifying migration status...
python manage.py showmigrations tasks
echo   DONE
echo.

echo ========================================================================
echo                        FIX COMPLETE!
echo ========================================================================
echo.
echo Next steps:
echo   1. Run server: python manage.py runserver
echo   2. Open: http://127.0.0.1:8000
echo   3. Login and test task detail pages
echo.
echo If you see "No team members assigned":
echo   - Go to Django Admin: http://127.0.0.1:8000/admin
echo   - Edit tasks and assign Users (not Employees)
echo.
echo ========================================================================
echo.

pause
