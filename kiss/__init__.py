from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
)

from .models.users import User, AuthenticatedUser
from .models.classification import ClassificationData


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    authnpolicy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authzpolicy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, authentication_policy=authnpolicy, authorization_policy=authzpolicy)
    config.include('pyramid_jinja2')
    config.include('cornice')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('verify','/verify')
    config.add_route('create', '/create')
    config.add_route('google_login', '/login/google')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
