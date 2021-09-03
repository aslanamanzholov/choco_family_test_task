# Python imports
from pathlib import Path
from .extra import *
import os
import logging
import sys

logger = logging.getLogger(__name__)


# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = Path(__file__).resolve(strict=True).parent.parent


# fetch the project_root
PROJECT_ROOT = DJANGO_ROOT.parent


# the name of the whole site
SITE_NAME = DJANGO_ROOT.name


# collect static files here
STATIC_ROOT = PROJECT_ROOT / 'static'


# collect media files here
MEDIA_ROOT = PROJECT_ROOT / 'media'


# look for static assets here
# STATICFILES_DIRS = [
#     PROJECT_ROOT / 'static',
# ]


# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    PROJECT_ROOT / 'templates',
]


# add apps/ to the Python path
sys.path.append(str(PROJECT_ROOT / 'apps'))
sys.path.append(str(PROJECT_ROOT / 'config'))

# ##### APPLICATION CONFIGURATION #########################


# set the project's default timezone
TIME_ZONE = 'Asia/Almaty'

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]


# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]



# The WSGI application to be used by Django's internal servers.
# Please note, Django's 'runserver' should **not** be used in production
# environments.
# If set to 'None', 'django.core.wsgi.get_wsgi_application()' will be used to
# determine the WSGI application.
WSGI_APPLICATION = os.environ.get('DPS_DJANGO_WSGI_APP', None)

# ASGI application
ASGI_APPLICATION = "config.routing.application"


# the root URL configuration
ROOT_URLCONF = '{}.urls'.format(SITE_NAME)


# the URL for static files
STATIC_URL = '/storage/'


# the URL for media files
MEDIA_URL = '/media/'

# Users settings
# AUTH_USER_MODEL = 'users.User'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# adjust the minimal login
# LOGIN_URL = 'core_login'
# LOGIN_REDIRECT_URL = os.environ.get('DPS_DJANGO_LOGIN_REDIRECT_URL', '/')
# LOGOUT_REDIRECT_URL = os.environ.get('DPS_DJANGO_LOGOUT_REDIRECT_URL', 'core_login')

# Internationalization
USE_I18N = False

# uncomment the following line to include i18n
from .i18n import *


# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = str(PROJECT_ROOT / 'run' / 'SECRET.key')


# these persons receive error notification
ADMINS = (
    ('A. Amanzholov', 'amanzholov.aslan@mail.ru'),
)
MANAGERS = ADMINS


# ##### DEBUG CONFIGURATION ###############################
DEBUG = False


# SITE

SECRET_KEY = os.environ.get('DPS_DJANGO_SECRET_KEY')

if SECRET_KEY is None:
    logger.debug('Could not find key in the environment!')

    logger.debug('Trying to read SECRET_KEY from SECRET_FILE...')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
        logger.info('Read SECRET_KEY from SECRET_FILE.')
    except IOError:
        logger.debug('Could not open SECRET_FILE ({})!'.format(SECRET_FILE))

        try:
            from django.utils.crypto import get_random_string
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
            SECRET_KEY = get_random_string(50, chars)
            with open(SECRET_FILE, 'w') as f:
                f.write(SECRET_KEY)

            logger.info('Generated a new SECRET_KEY and stored it in SECRET_FILE ({})!'.format(SECRET_FILE))
        except IOError:
            logger.exception('Could not open SECRET_FILE ({}) for writing!'.format(SECRET_FILE))
            raise Exception('Could not open {} for writing!'.format(SECRET_FILE))
else:
    logger.info('Fetched SECRET_KEY from environment.')
