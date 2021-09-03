# Django imports
from django.utils.translation import ugettext_lazy as _

# project imports
from .common import PROJECT_ROOT, MIDDLEWARE

# ##### INTERNATIONALIZATION ##############################

LANGUAGE_CODE = 'ru-RU'

# Internationalization
USE_I18N = True

# Localisation
USE_L10N = True

# enable timezone awareness by default
USE_TZ = True

# This list of languages will be provided
LANGUAGES = (
    ('ru-RU', _('Russian')),
)

# Look for translations in these locations
LOCALE_PATHS = (
    str(PROJECT_ROOT / 'locale'),
)

# Inject the localization middleware into the right position
MIDDLEWARE = [y for i, x in enumerate(MIDDLEWARE) for y in (
    ('django.middleware.locale.LocaleMiddleware', x) if MIDDLEWARE[i-1] == \
    'django.contrib.sessions.middleware.SessionMiddleware' else (x, ))]
