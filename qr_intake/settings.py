# qr_intake/settings.py (cabecera)
import os
from pathlib import Path

# Fallback elegante: usa python-decouple si está, si no usa os.getenv
try:
    from decouple import config as _config, Csv
    def ENV(key, default=None, cast=None):
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

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ENV("SECRET_KEY", "change_me")
DEBUG = ENV("DEBUG", "False") in ("True", "true", "1")

# Hosts y CSRF
ALLOWED_HOSTS = ENV("ALLOWED_HOSTS", "*")
if isinstance(ALLOWED_HOSTS, str):
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS.split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = ENV("CSRF_TRUSTED_ORIGINS", "")
if isinstance(CSRF_TRUSTED_ORIGINS, str) and CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in CSRF_TRUSTED_ORIGINS.split(",") if u.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

# Base de datos
DATABASE_URL = ENV(
    "DATABASE_URL",
    # Usa SIEMPRE la pública con sslmode=require en Railway
    "postgresql://postgres:TozCDNlDGOsuKyVZiOgqdezWndTwxZqv@gondola.proxy.rlwy.net:24947/railway?sslmode=require",
)

# Si tenés dj-database-url instalado, podés usar:
try:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
except Exception:
    # Fallback manual mínimo
    from urllib.parse import urlparse
    u = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": u.path.lstrip("/"),
            "USER": u.username,
            "PASSWORD": u.password,
            "HOST": u.hostname,
            "PORT": u.port or "5432",
            "OPTIONS": {"sslmode": "require"},
        }
    }

# Static con WhiteNoise
FORCE_WHITENOISE = ENV("FORCE_WHITENOISE", "True") in ("True", "true", "1")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] if os.path.isdir(os.path.join(BASE_DIR, "static")) else []

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    *(["whitenoise.middleware.WhiteNoiseMiddleware"] if FORCE_WHITENOISE else []),
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if FORCE_WHITENOISE:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }
