import datetime
AWS_GROUP_NAME = "HAUM_USER_GROUP"
AWS_USERNAME = "haum"
AWS_ACCESS_KEY_ID = "AKIAQR3FWRV63KBMU5HG"
AWS_SECRET_ACCESS_KEY = "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"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'G4Marketplace.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'G4Marketplace.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'haum'
S3DIRECT_REGION = 'ap-southeast-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}