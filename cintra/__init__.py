from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from cintra.models.models import appmaker
from cintra.models.security import groupfinder
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy( secret='topsecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory=root_factory, settings=settings)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
