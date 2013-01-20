import py.test

from tiddlyweb.config import config
from tiddlyweb.model.policy import UserRequiredError
from tiddlywebplugins.utils import (entitle, do_html, require_role,
        require_any_user)


STATUS = ''
HEADERS = []


def start_responser(status, headers, exc_info=None):
    global STATUS
    global HEADERS
    STATUS = status
    HEADERS = headers


def setup_module(module):
    module.environ = {'tiddlyweb.config': config}


def test_entitle():

    @entitle('monkey')
    def wsgi_app(environ, start_response):
        return ['monkey']

    assert 'tiddlyweb.title' not in environ

    output = wsgi_app(environ, start_responser)
    output = ''.join(output)
    assert '<title>TiddlyWeb - monkey</title>' in output

    assert 'tiddlyweb.title' in environ
    assert environ['tiddlyweb.title'] == 'monkey'

    @entitle('monkey')
    def wsgi_app(environ, start_response):
        return 'monkey'

    output = wsgi_app(environ, start_responser)
    output = ''.join(output)
    assert '<title>TiddlyWeb - monkey</title>' in output
    
    assert 'tiddlyweb.title' in environ
    assert environ['tiddlyweb.title'] == 'monkey'

    @entitle('monkey')
    def wsgi_app(environ, start_response):
        yield 'oh hi'
        return

    output = wsgi_app(environ, start_responser)
    output = ''.join(output)
    assert '<title>TiddlyWeb - monkey</title>' in output
    
    assert 'tiddlyweb.title' in environ
    assert environ['tiddlyweb.title'] == 'monkey'

def test_do_html():

    @do_html()
    def wsgi_app(environ, start_response):
        pass

    assert STATUS == ''

    wsgi_app(environ, start_responser)

    assert STATUS == '200 OK'
    assert ('Content-Type', 'text/html; charset=UTF-8') in HEADERS


def test_require_role():

    @require_role('ADMIN')
    def wsgi_app(environ, start_response):
        return 1

    with py.test.raises(UserRequiredError):
        wsgi_app(environ, start_responser)

    environ['tiddlyweb.usersign'] = {'roles': []}

    with py.test.raises(UserRequiredError):
        wsgi_app(environ, start_responser)

    environ['tiddlyweb.usersign'] = {'roles': ['fan']}

    with py.test.raises(UserRequiredError):
        wsgi_app(environ, start_responser)

    environ['tiddlyweb.usersign'] = {'roles': ['ADMIN']}

    output = wsgi_app(environ, start_responser)
    assert output == 1


def test_require_any_user():

    @require_any_user()
    def wsgi_app(environ, start_response):
        return 1

    with py.test.raises(UserRequiredError):
        wsgi_app(environ, start_responser)

    environ['tiddlyweb.usersign'] = {'name': 'GUEST'}

    with py.test.raises(UserRequiredError):
        wsgi_app(environ, start_responser)

    environ['tiddlyweb.usersign'] = {'name': 'monkey!'}

    output = wsgi_app(environ, start_responser)
    assert output == 1
