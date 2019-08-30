import os
import environ
# import oscar
from django.utils.translation import ugettext_lazy as _


env = environ.Env()

# Path helper
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', x)

if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = env.bool('DEBUG', default=False)
else:
    DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['oliviershop.herokuapp.com', 'localhost'])

EMAIL_SUBJECT_PREFIX = '[Olivier shop] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Make this unique, and don't share it with anybody.
SECRET_KEY = str(os.environ.get('SECRET_KEY', default='UajFCuyjDKmWHe29neauXzHi9eZoRXr6RMbT5JyAdPiACBP7Cra2'))

# Use a Sqlite database by default
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', location('db.sqlite3')),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
        'HOST': os.environ.get('DATABASE_HOST', None),
        'PORT': os.environ.get('DATABASE_PORT', None),
        'ATOMIC_REQUESTS': True
    }
}

CACHES = {
    'default': env.cache(default='locmemcache://'),
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'Africa/Casablanca'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr'

# Includes all languages that have >50% coverage in Transifex
# Taken from Django's default setting for LANGUAGES
gettext_noop = lambda s: s
LANGUAGES = (
    ('ar', gettext_noop('Arabic')),
    ('ca', gettext_noop('Catalan')),
    ('cs', gettext_noop('Czech')),
    ('da', gettext_noop('Danish')),
    ('de', gettext_noop('German')),
    ('en-gb', gettext_noop('British English')),
    ('el', gettext_noop('Greek')),
    ('es', gettext_noop('Spanish')),
    ('fi', gettext_noop('Finnish')),
    ('fr', gettext_noop('French')),
    ('it', gettext_noop('Italian')),
    ('ko', gettext_noop('Korean')),
    ('nl', gettext_noop('Dutch')),
    ('pl', gettext_noop('Polish')),
    ('pt', gettext_noop('Portuguese')),
    ('pt-br', gettext_noop('Brazilian Portuguese')),
    ('ro', gettext_noop('Romanian')),
    ('ru', gettext_noop('Russian')),
    ('sk', gettext_noop('Slovak')),
    ('uk', gettext_noop('Ukrainian')),
    ('zh-cn', gettext_noop('Simplified Chinese')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = location("media/public")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = location('static/public')

STATICFILES_DIRS = (
    location('static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# OSCAR_MISSING_IMAGE_URL = MEDIA_URL + 'public/'

if os.environ.get('ENV') == 'PRODUCTION':
    location = lambda x: os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', x)

    STATIC_ROOT = location('static/public/')
    STATIC_URL = '/static/public/'

    ADMIN_MEDIA_PREFIX = location('/media/public/')

    STATICFILES_DIRS = (
        # os.path.join(BASE_DIR, "static"),
        location('static/'),
        # location("media/public"),
    )

    AWS_S3_BUCKET_AUTH = False

    AWS_QUERYSTRING_AUTH = False

    AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365

    # AWS_DEFAULT_ACL = None

    OSCAR_MISSING_IMAGE_URL = "image_not_found.jpg"

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    # The AWS region to connect to.
    AWS_REGION = "us-west-1"

    # bucket name in
    AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME']

    # Préfixe à appliquer à chaque fichier stocké. Ce sera joint à chaque nom de fichier en utilisant le séparateur "/".
    # AWS_S3_KEY_PREFIX  =  "/"

    # Ce code n'a aucun effect sur stockage distant
    MEDIA_ROOT = 'http://s3.amazonaws.com/%s/media/public/' % AWS_S3_BUCKET_NAME

    MEDIA_URL = 'https://s3.amazonaws.com/%s/media/public' % AWS_S3_BUCKET_NAME

    #  See:http://stackoverflow.com/questions/10390244/
    # from storages.backends.s3boto3 import S3Boto3Storage
    # StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')  # noqa
    # MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media/public', file_overwrite=False)  # noqa
    # DEFAULT_FILE_STORAGE = 'store.settings.MediaRootS3BotoStorage'

    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

    # STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    # STATICFILES_STORAGE = "django_s3_storage.storage.ManifestStaticS3Storage"
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)


# from oscar import OSCAR_MAIN_TEMPLATE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates/'),
            # os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
            # OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            # ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

                # Oscar specific
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.core.context_processors.metadata',
            ],
            'debug': DEBUG,
        },
    }
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # Allow languages to be selected
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',

    # Ensure a valid basket is added to the request instance for every request
    'oscar.apps.basket.middleware.BasketMiddleware',
]

ROOT_URLCONF = 'urls'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'oscar': {
            'level': 'DEBUG',
            'propagate': True,
        },
        'oscar.catalogue.import': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'oscar.alerts': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },

        # Django loggers
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },

        # Third party
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sorl.thumbnail': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },

        # Papal conf
        'paypal.express': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'paypal.payflow': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# Les fonctionnalité desactivé
OSCAR_HIDDEN_FEATURES = ['oscar.apps.analytics', 'oscar.apps.checkout',
                         'oscar.apps.address', 'oscar.apps.shipping',
                         'oscar.apps.payment']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'oscar',
    'oscar.apps.analytics',
    'oscar.apps.checkout',
    'oscar.apps.address',
    'oscar.apps.shipping',
    'oscar.apps.catalogue',
    'oscar.apps.catalogue.reviews',
    'oscar.apps.partner',
    'oscar.apps.basket',
    'oscar.apps.payment',
    'oscar.apps.offer',
    'oscar.apps.order',
    'oscar.apps.customer',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'oscar.apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.orders',
    'oscar.apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',

    # 3rd-party apps that Oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'easy_thumbnails',
    'django_tables2',

    # Django apps that the sandbox depends on
    'django.contrib.sitemaps',

    # 3rd-party apps that the sandbox depends on
    'django_extensions',
    'debug_toolbar',

    # For allowing dashboard access
    # 'apps.gateway',

    # mon application
    # 'store',

    # Paypal
    # 'paypal',

    # aws django-s3-storage
    'django_s3_storage',
]

# Add Oscar's custom auth backend so users can sign in using their email
# address.
AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

# ====================
# Messages contrib app
# ====================

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': location('whoosh_index'),
    },
}
# Here's a sample Haystack config if using Solr (which is recommended)
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr/oscar_latest/',
#        'INCLUDE_SPELLING': True
#    },
#}

# =============
# Debug Toolbar
# =============

INTERNAL_IPS = ['127.0.0.1', '::1']

# ==============
# Oscar settings
# ==============

from oscar.defaults import *

# Meta
# ====

OSCAR_SHOP_TAGLINE = 'Sandbox'

OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_ALLOW_ANON_CHECKOUT = True

# Add Payflow dashboard stuff to settings
# OSCAR_DASHBOARD_NAVIGATION.append(
#     {
#         'label': _('PayPal'),
#         'icon': 'icon-globe',
#         'children': [
#             {
#                 'label': _('PayFlow transactions'),
#                 'url_name': 'paypal-payflow-list',
#             },
#             {
#                 'label': _('Express transactions'),
#                 'url_name': 'paypal-express-list',
#             },
#         ]
#     })

# Taken from PayPal's documentation - these should always work in the sandbox
PAYPAL_SANDBOX_MODE = True
PAYPAL_CALLBACK_HTTPS = False
# PAYPAL_API_VERSION = '95.0'

# These are the standard PayPal sandbox details from the docs - but I don't
# think you can get access to the merchant dashboard.
PAYPAL_API_USERNAME = 'oregonenew-facilitator_api1.gmail.com'
PAYPAL_API_PASSWORD = '6LXBCS2UJEDJ77GN'
PAYPAL_API_SIGNATURE = 'AHWrIJxqyN4RjJKikVA4Ghs6fBvKAvn.kWqFkORLVbZ1aw8BGyV6zvbA'

# Standard currency is GBP
PAYPAL_CURRENCY = PAYPAL_PAYFLOW_CURRENCY = 'EUR'
PAYPAL_PAYFLOW_DASHBOARD_FORMS = True

# Order processing
# ================

# Sample order/line status settings. This is quite simplistic. It's like you'll
# want to override the set_status method on the order object to do more
# sophisticated things.
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'

# This dict defines the new order statuses than an order can move to
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Complete', 'Cancelled',),
    'Cancelled': (),
    'Complete': (),
}

# This dict defines the line statuses that will be set when an order's status
# is changed
OSCAR_ORDER_STATUS_CASCADE = {
    'Being processed': 'Being processed',
    'Cancelled': 'Cancelled',
    'Complete': 'Shipped',
}

# LESS/CSS
# ========

# We default to using CSS files, rather than the LESS files that generate them.
# If you want to develop Oscar's CSS, then set OSCAR_USE_LESS=True to enable the
# on-the-fly less processor.
OSCAR_USE_LESS = False

# Currency
OSCAR_DEFAULT_CURRENCY = 'EUR'

OSCAR_SHOP_NAME = 'Olivier shop'

# Sorl
# ====

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_KEY_PREFIX = 'oscar-sandbox'
THUMBNAIL_KVSTORE = env(
    'THUMBNAIL_KVSTORE',
    default='sorl.thumbnail.kvstores.cached_db_kvstore.KVStore')
THUMBNAIL_REDIS_URL = env('THUMBNAIL_REDIS_URL', default=None)


# Django 1.6 has switched to JSON serializing for security reasons, but it does not
# serialize Models. We should resolve this by extending the
# django/core/serializers/json.Serializer to have the `dumps` function. Also
# in tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Security
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Try and import local settings which can be used to override any of the above.
try:
    from settings_local import *
except ImportError:
    pass
