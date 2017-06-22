from os import path, environ, getenv

from fabric.api import env
from fabric.colors import green

PROJECT_NAME = 'rookie_booking'

LINODEAPP1        = 'ross@lnapp1:832'
LINODEDB          = 'ross@lndb:832'

VAGRANTAPP1       = 'ross@vmapp1:22'
LOCALHOST_DESKTOP = 'UbuntuBox'
LOCALHOST_LAPTOP  = 'ross@UbuntuPad'

env.hosts = [LINODEAPP1,]
#env.hosts = [VAGRANTAPP1,]
#env.hosts = [VAGRANTAPP1, LINODEAPP]


VENV = PROJECT_NAME + 'Env'

PROJECT_USER = PROJECT_NAME + 'User'
#PROJECT_USER_PASSWORD = env_vars.PROJECT_USER_PASSWORD

REPO_URL = 'git@github.com:RossLYoung/rookie_booking.com.git'

ROOT_LOCATION = path.abspath('/www')

APP_DIR_BASE    = path.join(ROOT_LOCATION, 'apps')
SRC_DIR_BASE    = path.join(ROOT_LOCATION, 'src')
LOG_DIR_BASE    = path.join(ROOT_LOCATION, 'logs')
VENV_DIR_BASE   = path.join(ROOT_LOCATION, 'envs')
STATIC_DIR_BASE = path.join(ROOT_LOCATION, 'static')
MEDIA_DIR_BASE  = path.join(ROOT_LOCATION, 'media')
TMP_DIR_BASE    = path.join(ROOT_LOCATION, 'tmp')

APP_DIR    = path.join(APP_DIR_BASE, PROJECT_NAME)
SRC_DIR    = path.join(SRC_DIR_BASE, PROJECT_NAME)
LOG_DIR    = path.join(LOG_DIR_BASE, PROJECT_NAME)
VENV_DIR   = path.join(VENV_DIR_BASE, VENV)
STATIC_DIR = path.join(STATIC_DIR_BASE, PROJECT_NAME)
MEDIA_DIR  = path.join(MEDIA_DIR_BASE, PROJECT_NAME)
TMP_DIR    = path.join(TMP_DIR_BASE, PROJECT_NAME)


BASE_SERVER_DIRS = [
    APP_DIR_BASE,
    SRC_DIR_BASE,
    LOG_DIR_BASE,
    VENV_DIR_BASE,
    STATIC_DIR_BASE,
    MEDIA_DIR_BASE,
    TMP_DIR_BASE
]

PER_APP_DIRS = [
    APP_DIR,
    SRC_DIR,
    LOG_DIR,
    VENV_DIR,
    STATIC_DIR,
    MEDIA_DIR,
    TMP_DIR
]

REQUIREMENTS_FILE =  path.join(APP_DIR, 'requirements.txt')

DB_NAME             = PROJECT_NAME
DB_USER             = PROJECT_NAME + 'pguser'
DB_PASSWORD         = getenv('DB_PASSWORD','default_value')
DB_POSTGIS_REQUIRED = False
DB_DUMP_FILENAME = '{0}.dump'.format(PROJECT_NAME)
SERVER_DB_BACKUP_DIR = TMP_DIR

PG_ADMIN_ROLE = 'postgres'
#LOCAL_PG_USE_LOCALHOST = True

DEPLOY_BRANCH = 'master'

RSYNC_EXCLUDES = ['.git'] # no point having full repo history in app_dir

MAKEMESSAGES_ON_DEPLOYMENT = False
COMPILEMESSAGES_ON_DEPLOYMENT = False