
from pathlib import Path
import os
from dotenv import load_dotenv

# carrega os arquivos do .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# chave secreta do projeto (armazenado no .env)
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# instalar sempre o novo app criado
# 1- home
INSTALLED_APPS = [
    # apps do django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps do lib
    'apps.home.apps.HomeConfig',
    'apps.user_admin.apps.UserAdminConfig',
    'apps.login_perfil.apps.LoginPerfilConfig',
    'apps.filtros_buscas.apps.FiltrosBuscasConfig',
    'apps.user_bibliotecario.apps.UserBibliotecarioConfig',
    'apps.user_professor.apps.UserProfessorConfig',
    'apps.notificacao.apps.NotificacaoConfig',

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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'apps.filtros_buscas.context_processors.menu_filtro',
                'apps.user_bibliotecario.context_processors.perfil_bibliotecario_cp',
                'apps.user_professor.context_processors.perfil_professor_cp',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# banco de dados mysql (informações confidenciais no .env)
DATABASES = {
    'default': {
        'ENGINE': str(os.getenv('ENGINE')),
        'NAME': str(os.getenv('NAME')),
        'USER': str(os.getenv('USER')),
        'PASSWORD': str(os.getenv('PASSWORD')),
        'HOST': str(os.getenv('HOST')),
        'PORT': os.getenv('PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

# portugues br
LANGUAGE_CODE = 'pt-br'

# horario de SP
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# carregamento de estaticos

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'setup/static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# carregamento de midias

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
