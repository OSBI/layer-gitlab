from charmhelpers.core.hookenv import (
    relation_set,
    unit_get,
)
from charms.reactive import hook
from subprocess import check_call
from charmhelpers.core.hookenv import log

@hook('stop')
def remove_gitlab():
    check_call('apt-get', 'remove', 'gitlab-ce')


#@hook('website-relation-changed')
#def website_changed():
#    log("starting hook")
#    host = unit_get("private-address")
#    port = 8181
#    relation_set(hostname=host, port=port)
#   log("finished hook")
