python manage.py migrate
python manage.py collectstatic --no-input

gunicorn slovo.wsgi:application --bind 0.0.0.0:8000
