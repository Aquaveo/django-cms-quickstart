from pathlib import Path
import os
from django_storage_url import dsn_configured_storage_class

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "<a string of random characters>")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = [
    os.environ.get("DOMAIN"),
]
if DEBUG:
    ALLOWED_HOSTS = [
        "*",
    ]

# Redirect to HTTPS by default, unless explicitly disabled
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT") != "False"

X_FRAME_OPTIONS = "SAMEORIGIN"


# Application definition

INSTALLED_APPS = [
    "backend",
    # optional, but used in most projects
    "djangocms_admin_style",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # key django CMS modules
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    # Django Filer - optional, but used in most projects
    "filer",
    "easy_thumbnails",
    # the default CKEditor - optional, but used in most projects
    "djangocms_text_ckeditor",
    # some content plugins - optional, but used in most projects
    "djangocms_file",
    "djangocms_icon",
    "djangocms_picture",
    "djangocms_style",
    "djangocms_googlemap",
    "djangocms_video",
    "django_transfer",
    "djangocms_attributes_field",
    "djangocms_snippet",
    "djangocms_transfer",
    "djangocms_history",
    # optional django CMS Frontend modules
    "djangocms_frontend",
    "djangocms_frontend.contrib.accordion",
    "djangocms_frontend.contrib.alert",
    "djangocms_frontend.contrib.badge",
    "djangocms_frontend.contrib.card",
    "djangocms_frontend.contrib.carousel",
    "djangocms_frontend.contrib.collapse",
    "djangocms_frontend.contrib.content",
    "djangocms_frontend.contrib.grid",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.i18n",
                "cms.context_processors.cms_settings",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    #'easy_thumbnails.processors.scale_and_crop',
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)


CMS_TEMPLATES = [
    # a minimal template to get started with
    ("full-width.html", "Modern Bussiness"),
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Configure database using DATABASE_URL; fall back to sqlite in memory when no
# environment variable is available, e.g. during Docker build
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DJANGOCMS_DB_NAME"],
        "USER": os.environ["DJANGOCMS_DB_USER"],
        "PASSWORD": os.environ["DJANGOCMS_DB_PWD"],
        "HOST": os.environ["DJANGOCMS_DB_HOST"],
        "PORT": os.environ["DJANGOCMS_DB_PORT"],
    }
}


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "English"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.environ.get("STATIC_URL")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_collected")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
# DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

# read the setting value from the environment variable
DEFAULT_STORAGE_DSN = os.environ.get("DEFAULT_STORAGE_DSN")

# dsn_configured_storage_class() requires the name of the setting
DefaultStorageClass = dsn_configured_storage_class("DEFAULT_STORAGE_DSN")

# Django's DEFAULT_FILE_STORAGE requires the class name
DEFAULT_FILE_STORAGE = "backend.settings.DefaultStorageClass"

# only required for local file storage and serving, in development
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("/data/media/")

# FORCE_SCRIPT_NAME = '/meta/'
# LOGIN_REDIRECT_URL = '/meta/admin/'
# LOGOUT_REDIRECT_URL = '/meta/'
# LOGIN_URL="/admin/login/"

# USE_X_FORWARDED_HOST = True
SITE_ID = 1
TEXT_INLINE_EDITING = True

CKEDITOR_SETTINGS = {
    "styleSet": [
        {"name": "Italic Title", "element": "h2", "styles": {"font-style": "italic"}},
        {
            "name": "Subtitle",
            "element": "h3",
            "styles": {"color": "#aaa", "font-style": "italic"},
        },
        {
            "name": "Special Container",
            "element": "div",
            "styles": {
                "padding": "5px 10px",
                "background": "#eee",
                "border": "1px solid #ccc",
            },
        },
        {"name": "Strong", "element": "strong", "overrides": "b"},
        {"name": "Emphasis", "element": "em", "overrides": "i"},
        {"name": "Underline", "element": "u"},
        {"name": "Strikethrough", "element": "strike"},
        {"name": "Subscript", "element": "sub"},
        {"name": "Superscript", "element": "sup"},
        {
            "name": "Marker: Yellow",
            "element": "span",
            "styles": {"background-color": "Yellow"},
        },
        {
            "name": "Marker: Green",
            "element": "span",
            "styles": {"background-color": "Lime"},
        },
        {"name": "Big", "element": "big"},
        {"name": "Small", "element": "small"},
        {"name": "Typewriter", "element": "tt"},
        {"name": "Computer Code", "element": "code"},
        {"name": "Keyboard Phrase", "element": "kbd"},
        {"name": "Sample Text", "element": "samp"},
        {"name": "Variable", "element": "var"},
        {"name": "Deleted Text", "element": "del"},
        {"name": "Inserted Text", "element": "ins"},
        {"name": "Cited Work", "element": "cite"},
        {"name": "Inline Quotation", "element": "q"},
        {"name": "Language: RTL", "element": "span", "attributes": {"dir": "rtl"}},
        {"name": "Language: LTR", "element": "span", "attributes": {"dir": "ltr"}},
        {
            "name": "Styled image (left)",
            "element": "img",
            "attributes": {"class": "left"},
        },
        {
            "name": "Styled image (right)",
            "element": "img",
            "attributes": {"class": "right"},
        },
        {
            "name": "Compact table",
            "element": "table",
            "attributes": {
                "cellpadding": "5",
                "cellspacing": "0",
                "border": "1",
                "bordercolor": "#ccc",
            },
            "styles": {"border-collapse": "collapse"},
        },
        {
            "name": "Borderless Table",
            "element": "table",
            "styles": {"border-style": "hidden", "background-color": "#E6E6FA"},
        },
        {
            "name": "Square Bulleted List",
            "element": "ul",
            "styles": {"list-style-type": "square"},
        },
    ]
}
