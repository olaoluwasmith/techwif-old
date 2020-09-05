"""
Django settings for techsite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!fpr1f8%47-auv*+$t053on)ozn#7i&6t4vkjo+(836^=t38kn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'olaoluwasamsmith@gmail.com'
EMAIL_HOST_PASSWORD = 'Facebook1#'
ACCOUNT_EMAIL_VERIFICATION = 'none'

ALLOWED_HOSTS = ['smith-techwit.herokuapp.com', '127.0.0.1']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'tech.apps.TechConfig',
    'ecommerce.apps.EcommerceConfig',
    
    'storages',
    'notifications',
    'corsheaders',
    'crispy_forms',
    'django_social_share',
    'social_django',
    'taggit',
    'bootstrap4',
    'materializecssform',
]

PAYSTACK_PUBLIC_KEY = 'pk_live_02c89718098e7d151f27b9b1cb8e0bafc13ccfb9'
PAYSTACK_SECRET_KEY = 'sk_live_2de0f32557bb6bf49e04774528bf3886539faaec'

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  
]

ROOT_URLCONF = 'techsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = {
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',

    'django.contrib.auth.backends.ModelBackend',
}

SOCIAL_AUTH_FACEBOOK_KEY = '215610393159721' #App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '6adddd7006504d50ca83ba4f2a4d8fd4' #App Secret

WSGI_APPLICATION = 'techsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
#        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tech_1',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'olaoluwasmith',
        'PASSWORD': 'smithpython12',
        'HOST': 'database-1.ccshgogewdou.us-west-2.rds.amazonaws.com',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)
STATIC_URL = 'static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'static/media'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True }
DJANGO_NOTIFICATIONS_CONFIG = { 'SOFT_DELETE': True }


#S3 BUCKETS CONFIG
"""
AWS_ACCESS_KEY_ID = 'AKIAUHFMEN4AWKU4QYFC'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'olaoluwasmith-bucket'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
"""