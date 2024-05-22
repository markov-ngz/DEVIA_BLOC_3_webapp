python manage.py migrate --no-input
python manage.py tailwind install --no-input;
python manage.py tailwind build --no-input;
python manage.py collectstatic --no-input

gunicorn slovo.wsgi:application --bind 0.0.0.0:8000