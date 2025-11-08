web: gunicorn qr_intake.wsgi:application --workers=1 --threads=2 --timeout=120 --graceful-timeout=30 --max-requests=200 --max-requests-jitter=50 --log-level=info
