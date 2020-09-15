from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

#S3 BUCKETS CONFIG
"""
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AKIAUHFMEN4AQCSIQRXS')
    AWS_SECRET_ACCESS_KEY = os.getenv('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')
    AWS_STORAGE_BUCKET_NAME = os.getenv('techwit')
    AWS_MEDIA_BUCKET_NAME = os.getenv('techwit')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}'
    STATICFILES_STORAGE = 'techsite.custom_storages.StaticStorage'

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}'
    DEFAULT_FILE_STORAGE = 'techsite.custom_storages.MediaStorage'

else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


AWS_ACCESS_KEY_ID = 'AKIAUHFMEN4AQCSIQRXS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'techwit'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'techsite.custom_storages.StaticStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'techsite.custom_storages.MediaStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)
"""