web: gunicorn qr_intake.wsgi:application --bind 0.0.0.0:$PORT --workers=${WEB_CONCURRENCY:-2} --threads=${WEB_THREADS:-1} --timeout=${WEB_TIMEOUT:-120}
