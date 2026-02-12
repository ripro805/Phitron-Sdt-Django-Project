@echo off
echo ============================================================
echo Fixing Database Migration Error
echo ============================================================
echo.

cd /d "d:\KnowledgeVault\Practice\Phitron-SDT-Course-\Development\Django\Django Project\task_management"

echo Activating virtual environment...
call task_env\Scripts\activate.bat

echo.
echo Running migration to fix assigned_to table...
python manage.py migrate tasks 0006_fix_assigned_to_table

echo.
echo ============================================================
echo Migration Complete!
echo ============================================================
echo.
echo Now you can run: python manage.py runserver
echo.

pause
