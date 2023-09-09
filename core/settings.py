from pathlib import Path
import os
import socket


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v2_d#nv6ls^j+a0z457$xr##kt1s)40u__pew2jkh%d*01)+s='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Define manualmente la URL de GitHub CodeSpaces
github_codespace_url = "https://crispy-space-succotash-67wg5q4jrj5hxxjx-8000.app.github.dev"

# Divide la URL para extraer el nombre del entorno y el dominio
github_codespace_parts = github_codespace_url.split(".")
github_codespace_name = github_codespace_parts[0].replace("https://", "")
github_codespace_domain = ".".join(github_codespace_parts[1:])

# Define la lista de orígenes permitidos para CSRF
CSRF_TRUSTED_ORIGINS = []

# Agrega localhost:8000 como origen permitido (útil para desarrollo local)
CSRF_TRUSTED_ORIGINS.append("http://localhost:8000")
CSRF_TRUSTED_ORIGINS.append("https://localhost:8000")  # También permitimos HTTPS

# Si se está ejecutando en GitHub CodeSpaces, agrega la URL de GitHub CodeSpaces como origen permitido
if github_codespace_name and github_codespace_domain:
    github_codespace_url = f"https://{github_codespace_name}-8000.{github_codespace_domain}"
    CSRF_TRUSTED_ORIGINS.append(github_codespace_url)

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
#SE SEPARO EN LISTAS PARA LLEVAR MEJOR ORDEN 

#APPS LOCALES
LOCAL_APPS = ['accounts','login','servicio','cliente',]

#API
API_REST = ['api',]

#LIRERIAS
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + API_REST + THIRD_PARTY_APPS


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# En el archivo CORS_ORIGIN_WHITELIST, también asegúrate de permitir ambas versiones de localhost
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'https://localhost:4200',  # También permitimos HTTPS
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'core.urls'
X_FRAME_OPTIONS = "ALLOW-FROM preview.app.github.dev"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-CL'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = False



#CORREOS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'alnso.arizona@gmail.com' 
EMAIL_HOST_PASSWORD = 'vtjpbhmyixxcakdr'




STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

AUTH_USER_MODEL = 'accounts.User'



