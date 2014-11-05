# This script drops and recreates your database and then runs migrations
echo "If any errors occur while this script is running then it did not execute properly"
dropdb revolv_db
echo "Database revolv_db has been dropped"
createdb -U revolv -E utf8 -O revolv revolv_db -h localhost
echo "Database revolv_db has been created"
python manage.py migrate
echo "Migrations have been run"
