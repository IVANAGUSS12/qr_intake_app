# Deploy en Railway — QR Intake App

## 1) Subir a GitHub
Subí este proyecto a un repo (público o privado).

## 2) Crear proyecto y base en Railway
- New Project → Deploy from GitHub Repo.
- Add → Database → PostgreSQL (copiá `DATABASE_URL`).

## 3) Variables de entorno (Service Web)
Agregá estas variables:
```
DEBUG=False
SECRET_KEY=<algo-largo-y-seguro>
ALLOWED_HOSTS=*
FORCE_WHITENOISE=True
DATABASE_URL=<tu DATABASE_URL de Railway>
USE_S3=True
AWS_ACCESS_KEY_ID=<tu key>
AWS_SECRET_ACCESS_KEY=<tu secret>
AWS_STORAGE_BUCKET_NAME=<tu bucket>
AWS_S3_REGION_NAME=nyc3
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```
> Si no tenés S3/Spaces todavía, podés iniciar con `USE_S3=False` (no recomendado en PaaS por ser efímero).

## 4) Build / Start
- Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start: `gunicorn qr_intake.wsgi:application -c gunicorn.conf.py`

## 5) Migraciones y seed
En la Shell del servicio:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo   # opcional: crea Servicios y Médicos de prueba
```

## 6) Rutas
- Formulario QR: `/qr/intake/`
- Panel (tabs por servicio): `/panel/` y `/panel/<slug>/`
- Admin: `/admin/`
