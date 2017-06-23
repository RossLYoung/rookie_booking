from os import path, listdir, environ

from fabric.api import env, run, cd, lcd, local, settings as settings_context_manager, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import append
from fabric.colors import green, red
from fabric.contrib import django as fab_django
from fabtools import require, supervisor, nginx, service, postgres
from fabtools.python import virtualenv

from ..env_vars import vars
for key, val in vars.items():
   environ.setdefault(key,val)

from django.conf import settings

#Tell fabric where settings are
fab_django.settings_module('rookie_booking.settings')

# Allows configurations to work properly - django.conf.settings now work
from configurations import importer
importer.install()

#This allows agent forwarding
env.use_ssh_config = True
env.forward_agent = True


def get_nginx_ssl(host_name):

    NGINX_SSL_CONFIG = {
        "SSL_PRIVATE_KEY": None,
        "SSL_CERTIFICATE": None,
        "NGINX_CONFIG": "nginx.conf",
    }

    if settings.PROJECT_NAME == "rosslyoung":
        print(green("Personal site on personal Linode"))
        NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"] = "rosslyoung.com.key"
        NGINX_SSL_CONFIG["SSL_CERTIFICATE"] = "rosslyoung.com.crt"
        NGINX_SSL_CONFIG["NGINX_CONFIG"] = "nginx.conf"
    elif "lnapp" in host_name:
        print(green("Client Site on personal Linode, so use RLY SSL as this is on a subdomain"))
        NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"] = None
        NGINX_SSL_CONFIG["SSL_CERTIFICATE"] = None
        NGINX_SSL_CONFIG["NGINX_CONFIG"] = "nginx.conf"
    else:
        print(green("Client Site not on personal Linode"))
        NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"] = None
        NGINX_SSL_CONFIG["SSL_CERTIFICATE"] = None
        NGINX_SSL_CONFIG["NGINX_CONFIG"] = "nginx.conf"

    return NGINX_SSL_CONFIG

#####################################################################

def do_all():
    pre_bootstrap()
    app_bootstrap()
    deploy()


def pre_bootstrap():
    require.user('webapps', create_home=False, system=True, group='webapps')
    require.files.directories(settings.BASE_SERVER_DIRS, use_sudo=True, owner=env.user, group='webapps')


def yolo():

    print "yolo yo!"

def app_bootstrap():

    #ToDo: Prompt for DB & DB user creation - Handle DB already exists
    add_user()
    create_app_dirs()
    create_log_files()
    venv_wrapper_shell()
    create_venv()
    supervisor_config()
    ssl_keys()
    nginx_config()
    nginx_enable()

def db_bootstrap():
    add_pg_user()
    create_database(postgis=settings.DB_POSTGIS_REQUIRED)


def deploy():
    #ToDo: settings.DEBUG check

    #ToDo: This needs to happen before git add . Otherwise, 2 deploys needed to get updated req.txt onto server
    #ToDo: Git add, commit, push would work, but want to deploy what is on git and therefore tested on dev

    #make_migrations()
    #pip_freeze()

    # Remote
    git_pull()
    add_env_vars_to_activate() # this should copy file over, export, then delete file - No need to ever be in vcs
    rsync()
    delete_src()
    install_requirements()
    # syncdb()
    ssl_keys()
    nginx_config()

    #makemigrations()
    migrate()
    collectstatic()
    set_app_dirs_permissions()
    restart_supervisor()
    restart_nginx()

#ToDo: Nuke function to delete app dirs, Ngingx symlinks, and Supervisor config

def import_remote_db():
    """
    Downloads the prod db and imports it locally.
    """
    run_export_db()
    run_download_db()
    drop_db()
    create_database(postgis=True)
    import_db()
    #reset_passwords()

################################################################
#######################App Bootstrap ###########################
################################################################

def add_user():
    print(green("Adding user"))
    require.user(settings.PROJECT_USER, create_home=False, system=True, group='webapps')

def add_pg_user():
    print(green("Adding Postgres user - " + settings.DB_USER))
    #print(postgres.user_exists(DB_USER)) # doesn't check correctly
    if not postgres.user_exists(settings.DB_USER):
        postgres.create_user(settings.DB_USER, password=settings.DB_PASSWORD, encrypted_password=True)

    #require.postgres.user(DB_USER, DB_PASSWORD, encrypted_password=True)

def create_database(postgis=False):
    """
    postgis=false if creating a fresh DB to pg_restore a DB which already has postgis installed - spheroid already exists error
    """
    print(green("Creating PG database"))
    if not postgres.database_exists(settings.DB_NAME):
        require.postgres.database(settings.DB_NAME,
                                  settings.DB_USER,
                                  #locale='en_GB.utf8',
                                  locale='en_GB.UTF-8',
                                  template="template_postgis" if postgis else 'template0'
    )


def create_app_dirs():
    print(green("Creating app directories"))
    require.files.directories(settings.PER_APP_DIRS, use_sudo=True, owner=settings.PROJECT_USER, group='webapps', mode=770) #


def create_log_files():
    print(green("Creating log files"))
    require.files.file(path.join(settings.LOG_DIR,'application.log')     ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770 )
    require.files.file(path.join(settings.LOG_DIR,'gunicorn-access.log') ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770 )
    require.files.file(path.join(settings.LOG_DIR,'gunicorn-error.log')  ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770 )
    require.files.file(path.join(settings.LOG_DIR,'nginx-access.log')    ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770)
    require.files.file(path.join(settings.LOG_DIR,'nginx-error.log')     ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770)
    require.files.file(path.join(settings.LOG_DIR,'supervisor.log')      ,use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770)
    require.files.file(path.join(settings.LOG_DIR,'supervisor-error.log'),use_sudo=True, owner=settings.PROJECT_USER, group='webapps',mode=770)


def venv_wrapper_shell():
    '''
    The fabric user needs to have venvwrapper functions available to the shell (mkvirtualenv etc)
    '''
    print(green("Enabling venvwrapper"))
    bashrc = path.join('$HOME','.bashrc')
    append(bashrc,'source /usr/local/bin/virtualenvwrapper.sh',use_sudo=True)


def create_venv():
    print(green("Creating venv"))
    with prefix("source ~/.bashrc"): # Enable mkvirtualenv function as it's in a non default location
        require.python.virtualenv(settings.VENV_DIR, use_sudo=True, user=settings.PROJECT_USER)
        sudo('chgrp -R webapps {0}'.format(settings.VENV_DIR))
        sudo('chmod -R g+rwx {0}'.format(settings.VENV_DIR))
        sudo('chmod -R g+rwx {0}'.format(settings.APP_DIR))

def supervisor_config():
    print(green("Adding Supervisor config file"))
    source = path.join(settings.BASE_DIR, settings.PROJECT_NAME, 'config/supervisor.conf') #ToDo: fix assumption that project has app with same name - perhaps a main App  setting?
    file_path = '/etc/supervisor.d/{0}.conf'.format(settings.PROJECT_NAME)
    require.file(path=file_path, source=source, use_sudo=True, owner=settings.PROJECT_USER, group='webapps')
    #If ever this function fails, ensure /etc/ssh/sshd_config has 'Subsystem sftp internal-sftp' or similar - very hard to diagnose error


def ssl_keys():
    print (green("SSL...."))

    NGINX_SSL_CONFIG = get_nginx_ssl(env.host_string)
    if not NGINX_SSL_CONFIG['SSL_CERTIFICATE']: # Client Site on personal Linode
        print(green("Client project on personal server - no need to copy SSL cert/key")) #don't copy this projects SSL as it is handled by rosslyoung.com project - this is on a subdomain
    else:
        print(green("Adding SSL cert/key"))
        print(green(NGINX_SSL_CONFIG["SSL_CERTIFICATE"]))
        print(green(NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"]))
        crt = path.join(settings.BASE_DIR, settings.PROJECT_NAME,      'config/ssl/', NGINX_SSL_CONFIG["SSL_CERTIFICATE"])  #ToDo: fix assumption that project has app with same name.....
        key = path.join(settings.BASE_DIR, settings.PROJECT_NAME,      'config/ssl/', NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"])  #ToDo: fix assumption that project has app with same name.....
        key_pass = path.join(settings.BASE_DIR, settings.PROJECT_NAME, 'config/ssl/key_pass')                               #ToDo: fix assumption that project has app with same name.....
        crt_file_path = '/etc/nginx/ssl/' + NGINX_SSL_CONFIG["SSL_CERTIFICATE"]
        key_file_path = '/etc/nginx/ssl/' + NGINX_SSL_CONFIG["SSL_PRIVATE_KEY"]
        # key_pass_path = '/etc/nginx/ssl/key_pass'
        require.directory('/etc/nginx/ssl', owner='root', use_sudo=True, mode=700)
        require.file(path=crt_file_path, source=crt, use_sudo=True, mode=600, owner='root', group='root')
        require.file(path=key_file_path, source=key, use_sudo=True, mode=600, owner='root', group='root')
        # require.file(path=key_pass_path, source=key_pass, use_sudo=True, mode=600, owner='root', group='root')


def nginx_config():
    print(green("Creating Nginx symlink to config file"))
    NGINX_SSL_CONFIG = get_nginx_ssl(env.host_string)

    target = '/etc/nginx/sites-available/{0}'.format(settings.PROJECT_NAME)
    source = path.join(settings.APP_DIR, settings.PROJECT_NAME, 'config/', NGINX_SSL_CONFIG["NGINX_CONFIG"]) #ToDo: fix assumption that project has app with same name - perhaps a main App  setting?
    sudo('ln -sf {0} {1}'.format(source, target))


#using require should reload nginx config, unlike those above
def nginx_enable():
    print(green("Enabling site in Nginx"))
    require.nginx.enabled(settings.PROJECT_NAME)


def nginx_disable():
    print(green("Disabling site in Nginx"))
    require.nginx.disabled(settings.PROJECT_NAME)

################################################################
##################### Deploy ###################################
################################################################

def run_tests():
    #local("./manage.py test my_app")
    pass


def git_commit():
    local("git add -p && git commit")


def pip_freeze():
    print(green("Pip Freeze"))
    with lcd(settings.BASE_DIR):
        local('pip freeze > requirements.txt')


def git_push():
    local("git push origin {0}".format(settings.DEPLOY_BRANCH))


def git_pull():
    with settings_context_manager(warn_only=True):
        if run("test -d {0}".format(path.join(settings.SRC_DIR, '.git'))).failed:
            with settings_context_manager( use_sudo=True, user=env.user): #don't change user - needed for ssh key forwarding
                print(green("Cloning repository with " + env.user))
                run("git clone {0} {1}".format(settings.REPO_URL, settings.SRC_DIR))
        else:
            with cd(settings.SRC_DIR):
                print(green("Pulling from repository"))
                with settings_context_manager( use_sudo=True):
                    run("git pull")


def rsync():
    print(green("Rsync SRC to app directory"))
    excludes = ''
    for exclude in settings.RSYNC_EXCLUDES:
        excludes += " --exclude '{0}'".format(exclude)
    command = "rsync -avz --stats --delete {0} {1}/ {2}".format(excludes, settings.SRC_DIR, settings.APP_DIR)

    sudo(command)

# def delete_src():
#     print(green("Removing Source"))
#     with cd(settings.SRC_DIR_BASE):
#         sudo('rm -r {0}'.format(settings.SRC_DIR))
#         with settings_context_manager(user=settings.PROJECT_USER):
#             sudo('mkdir {0}'.format(settings.SRC_DIR))

#don't delete folder as above, just the contents
def delete_src():
    print(green("Removing Source"))
    with cd(settings.SRC_DIR):
        sudo('rm -rf .git .gitignore *')

def install_requirements():
    print(green("Installing requirements"))
    #with settings_context_manager(user=PROJECT_USER):
    with virtualenv(settings.VENV_DIR):
        require.python.requirements(settings.REQUIREMENTS_FILE)


def add_env_vars_to_activate(env_location=settings.VENV_DIR):
    print(green("Appending environment variables to venv activate script"))
    activate = path.join(env_location,'bin/activate')

    for key, val in vars.items():
        append(activate,'export {k}={v}'.format(k=key, v=val) ,use_sudo=True)

def syncdb():
    print(green("Syncronising database"))
    with virtualenv(settings.VENV_DIR):
        with cd(settings.APP_DIR):
            run('python manage.py syncdb')

def make_migrations():
    print(green("Create database migrations"))
    with virtualenv(settings.VENV_DIR):
        with cd(settings.APP_DIR):
            run('python manage.py makemigrations')

def makemigrations():
    print(green("Running makemigrations"))
    with virtualenv(settings.VENV_DIR):
        with cd(settings.APP_DIR):
            run('python manage.py makemigrations')

def migrate():
    print(green("Running database migrations"))
    with virtualenv(settings.VENV_DIR):
        with cd(settings.APP_DIR):
            run('python manage.py migrate')


def collectstatic():
    print(green("Collecting static files to STATIC_ROOT"))
    with virtualenv(settings.VENV_DIR):
        with cd(settings.APP_DIR):
            sudo('python manage.py collectstatic --noinput')


def set_app_dirs_permissions():
    print(green("Tightening permissions for all application directories"))
    for dir in settings.PER_APP_DIRS:
        #if dir not in [settings.SRC_DIR]: #already deleted src_dir
        sudo('chown -R {0}:webapps {1}'.format(settings.PROJECT_USER, dir))
        sudo('chmod -R 770 {0}'.format(dir))


def restart_supervisor():
    print(green("Restating Supervisor"))
    supervisor.update_config()
    supervisor.restart_process(settings.PROJECT_NAME)


def restart_nginx():
    print(green("Restarting Nginx"))
    if service.is_running('nginx'):
        #service.restart('nginx')
        service.reload('nginx')
    else:
        service.start('nginx')


################################################################
############### DB - Dump Restore etc ##########################
################################################################


#########################################################
#########################################################
############# Utility Functions #########################
#########################################################
#########################################################

def supervisor_status(name):
    return supervisor.process_status(name)


def clear_logs():
    for f in listdir(settings.LOG_DIR):
        if f[-1] != "~":
            with open(path.join(settings.LOG_DIR, str(f)), 'w') as opened_file:
                pass
