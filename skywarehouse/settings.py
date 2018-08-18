"""Generated by 'django-admin startproject' using Django 1.11.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Security settings

SECRET_KEY = 'DevKey'

DEBUG = True

ALLOWED_HOSTS = ["localhost", "skywarehouse.herokuapp.com", ".skyware.house", ".amazonaws.com"]


# Application definition

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'materialize_forms',
    'storages',
    'warehouse',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skywarehouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # Manual Edit
            ],
        },
    },
]

AUTH_USER_MODEL = 'warehouse.User'

WSGI_APPLICATION = 'skywarehouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'          },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'         },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'        }
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATH = (
    os.path.join(BASE_DIR, "locale"),
)


# AWS settings

AWS_ACCESS_KEY_ID = ""

AWS_SECRET_ACCESS_KEY = ""

AWS_STORAGE_BUCKET_NAME = ""

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_LOCATION = 'staticfiles'


# Media files (uploads)
# https://docs.djangoproject.com/en/1.8/

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_LOCATION = 'media'


# Mail

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Prod settings

if os.environ.get("PROD") == 'TRUE':
    print("Production settings found, overriding dev settings.")

    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

    SECRET_KEY = os.environ.get("SECRET_KEY")

    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_KEY")

    DEBUG = False

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.gandi.net'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'accounts@skyware.house'
    EMAIL_HOST_PASSWORD = os.environ.get("MAIL_PWD")
    EMAIL_USE_TLS = True

    STATICFILES_STORAGE = 'skywarehouse.custom_storages.StaticStorage'

    DEFAULT_FILE_STORAGE = 'skywarehouse.custom_storages.MediaStorage'

    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIA_LOCATION)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'class': 'logging.StreamHandler'}},
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR')
            }
        }
    }

else:
    print("No production settings found, using dev settings.")
