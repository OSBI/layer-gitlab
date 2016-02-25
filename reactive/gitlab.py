import fileinput
import sys
from charmhelpers.fetch import apt_install
from charms.reactive import when, when_not, set_state, remove_state, hook
from subprocess import check_call, CalledProcessError, call
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set
from charms.reactive.helpers import data_changed
import re
import shutil


@when_not('gitlab.installed')
def install():
    status_set('maintenance', 'Installing GitLab')
    apt_install(["curl", "openssh-server", "ca-certificates", "postfix"])

    check_call(['apt-key', 'add', './data/gitlab_gpg.key'])

    shutil.copy2('data/gitlab_gitlab-ce.list', '/etc/apt/sources.list.d/gitlab-ce.list')

    check_call(['apt-get', 'update'])

    version = ''
    if hookenv.config('gitlab_version'):
        version = '=' + hookenv.config('gitlab_version')

    check_call(['apt-get', 'install', 'gitlab-ce' + version])
    check_call(['gitlab-ctl', 'reconfigure'])
    set_state('gitlab.installed')
    status_set('active', 'GitLab is ready!')


@when('gitlab.installed')
def check_running():
    if data_changed('gitlab.config', hookenv.config()):
        status_set('maintenance', 'Updating Config')
        updateConfig(hookenv.config())

    if hookenv.config('http_port'):
        hookenv.open_port(hookenv.config('http_port'))
    else:
        hookenv.open_port(80)

    status_set('active', 'GitLab is ready!')


def updateConfig(config):
    filepath = '/etc/gitlab/gitlab.rb'

    exturl = None

    if hookenv.config('external_url'):
        exturl = hookenv.config('external_url')
        if not exturl.startswith("http"):
            exturl = "http://" + exturl

    if hookenv.config('external_url') and hookenv.config('http_port'):
        if exturl.endswith("/"):
            exturl = exturl[:-1]

        exturl = exturl + ":" + hookenv.config('http_port')

    modConfigNoEquals(filepath, 'external_url', exturl)
    modConfig(filepath, 'gitlab_rails[\'gitlab_ssh_host\']', hookenv.config('ssh_host'))
    modConfig(filepath, 'gitlab_rails[\'time_zone\']', hookenv.config('time_zone'))
    modConfig(filepath, 'gitlab_rails[\'gitlab_email_from\']', hookenv.config('email_from'))
    modConfig(filepath, 'gitlab_rails[\'gitlab_email_display_name\']', hookenv.config('from_email_name'))
    modConfig(filepath, 'gitlab_rails[\'gitlab_email_reply_to\']', hookenv.config('reply_to_email'))
    modConfig(filepath, 'gitlab_rails[\'smtp_enable\']', hookenv.config('smtp_enable'))
    modConfig(filepath, 'gitlab_rails[\'smtp_address\']', hookenv.config('smtp_address'))
    modConfig(filepath, 'gitlab_rails[\'smtp_port\']', hookenv.config('smtp_port'))
    modConfig(filepath, 'gitlab_rails[\'smtp_user_name\']', hookenv.config('smtp_user_name'))
    modConfig(filepath, 'gitlab_rails[\'smtp_password\']', hookenv.config('smtp_password'))
    modConfig(filepath, 'gitlab_rails[\'smtp_domain\']', hookenv.config('smtp_domain'))
    modConfig(filepath, 'gitlab_rails[\'smtp_enable_starttls_auto\']', hookenv.config('smtp_enable_starttls_auto'))
    modConfig(filepath, 'gitlab_rails[\'smtp_tls\']', hookenv.config('smtp_tls'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_enabled\']', hookenv.config('incoming_email_enabled'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_address\']', hookenv.config('incoming_email_address'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_email\']', hookenv.config('incoming_email_email'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_password\']', hookenv.config('incoming_email_password'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_host\']', hookenv.config('incoming_email_host'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_port\']', hookenv.config('incoming_email_port'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_ssl\']', hookenv.config('incoming_email_ssl'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_start_tls\']', hookenv.config('incoming_email_start_tls'))
    modConfig(filepath, 'gitlab_rails[\'incoming_email_mailbox_name\']', hookenv.config('incoming_email_mailbox_name'))
    modConfig(filepath, 'gitlab_rails[\'backup_path\']', hookenv.config('backup_path'))
    modConfig(filepath, 'gitlab_rails[\'backup_keep_time\']', hookenv.config('backup_keep_time'))
    modConfig(filepath, 'gitlab_rails[\'backup_upload_remote_directory\']',
              hookenv.config('backup_upload_remote_directory'))
    modConfig(filepath, 'gitlab_rails[\'backup_upload_connection\']', hookenv.config('backup_upload_connection'))

    check_call(["gitlab-ctl", "reconfigure"])

    status_set('active', 'GitLab is ready!')


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def modConfigNoEquals(File, Variable, Setting):
    for line in fileinput.input(File, inplace=1):
        if line.startswith(Variable):
            line = Variable + ' \'' + Setting + '\''
        sys.stdout.write(line)
    fileinput.close()


def modConfig(File, Variable, Setting):
    """
    Modify Config file variable with new setting
    """
    VarFound = False
    AlreadySet = False
    V = str(Variable)
    S = str(Setting)
    if isinstance(Setting, bool):
        if (Setting):
            S = "true"
        else:
            S = "false"
    elif (S.isdigit()):
        S = int(S)
    elif (isfloat(S)):
        S = float(S)
    else:
        S = '\'' + S + '\''

    for line in fileinput.input(File, inplace=1):
        # process lines that look like config settings #
        if '=' in line:
            _infile_var = str(line.split('=')[0].rstrip(' '))
            _infile_set = str(line.split('=')[1].lstrip(' ').rstrip())
            # only change the first matching occurrence #
            if VarFound == False and _infile_var.rstrip(' ') == V:
                VarFound = True
                # don't change it if it is already set #
                if _infile_set.lstrip(' ') == S:
                    AlreadySet = True
                else:
                    line = "%s = %s\n" % (V, S)

        sys.stdout.write(line)

    # Append the variable if it wasn't found #
    if not VarFound:
        print("Variable '%s' not found.  Adding it to %s" % (V, File))
        with open(File, "a") as f:
            l = "%s = %s\n" % (V, S)
            if (Setting is '' or Setting is None) and not l.lstrip(' ').startswith('#'):
                l = '#' + l
                f.write(l)
            elif (Setting is not '' or Setting is not None) and l.lstrip(' ').startswith('#'):
                l = re.sub("#", "", l)
                f.write(l)
            elif (Setting is not '' or Setting is not None):
                f.write(l)

    elif AlreadySet == True:
        print("Variable '%s' unchanged" % (V))
    else:
        print("Variable '%s' modified to '%s'" % (V, S))

    fileinput.close()
    return
