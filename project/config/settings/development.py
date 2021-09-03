# Python imports
import os
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

# fetch the common settings
from .common import *
from .extra import *

# ##### APPLICATION CONFIGURATION #########################

# allow all hosts during development
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = DEFAULT_APPS
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    # apps
    'users',
    'utils',
    'tasks',
]

MIDDLEWARE = [
    *MIDDLEWARE,
]

#### DATABASE CONFIGURATION ############################

DATABASES = {'default': env.db()}

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True
