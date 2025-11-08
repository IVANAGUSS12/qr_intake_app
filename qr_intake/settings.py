import os
import dj_database_url
from pathlib import Path

# ======================================================
# 🔧 CONFIGURACIÓN BASE
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# --- helper ENV (fix cast=None) ---
try:
    from decouple import config as _config
    def ENV(key, default=None, cast=None):
        if cast is None:
            return _config(key, default=default)
        return _config(key, default=default, cast=cast)
except Exception:
    def ENV(key, default=None, cast=None):
        val = os.getenv(key, default)
        if cast is not None and val is not None:
            if cast is bool:
                return str(val).lower() in ("1", "true", "yes", "on")
            if cast is list:
                return [x.strip() for x in str(val).split(",") if x.strip()]
        return val
# --- fin helper ENV ---

# ======================================================
# 🔐 CLAVES Y DEBUG
# ======================================================

SECRET_KEY = ENV("SECRET_KEY", "change_me")
DEBUG = ENV("DEBUG", False, cast=bool)
ALLOWED_HOSTS = ENV("ALLOWED_HOSTS", "*", cast=list)

# ======================================================
# 📦 APLICACIONES
# ======================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "intake",
]

# ======================================================
# 🔧 MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "qr_intake.urls"
WSGI_APPLICATION = "qr_intake.wsgi.application"

# ======================================================
# 🗄️ BASE DE DATOS (Railway)
# ======================================================

DATABASE_URL = ENV("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# ======================================================
# 🌐 INTERNACIONALIZACIÓN
# ======================================================

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# ======================================================
# 📁 ARCHIVOS ESTÁTICOS
# ======================================================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Para servir archivos estáticos con WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ======================================================
# 📧 CSRF Y DOMINIOS
# ======================================================

CSRF_TRUSTED_ORIGINS = ENV("CSRF_TRUSTED_ORIGINS", "", cast=list)

# ======================================================
# ☁️ S3 / DigitalOcean (opcional)
# ======================================================

USE_S3 = ENV("USE_S3", False, cast=bool)

if USE_S3:
    AWS_STORAGE_BUCKET_NAME = ENV("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = ENV("AWS_S3_REGION_NAME", "nyc3")
    AWS_S3_ENDPOINT_URL = ENV("AWS_S3_ENDPOINT_URL", "https://nyc3.digitaloceanspaces.com")
    AWS_ACCESS_KEY_ID = ENV("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = ENV("AWS_SECRET_ACCESS_KEY")

# ======================================================
# 🔊 LOGGING SIMPLE (para depuración)
# ======================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
