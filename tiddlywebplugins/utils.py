"""
A suite of tools that make creating and handling plugins
in TiddlyWeb a bit more sensible.

Essentially this is a way to raise duplication to a common
core without encumbering the TiddlyWeb core.

See also http://tiddlyweb.com and http://github.com/tiddlyweb
"""

import os

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import UserRequiredError
from tiddlyweb.store import NoBagError


def entitle(title):
    """
    Decorator that sets tiddlyweb.title in environ.
    """

    def entangle(handler):

        def _entitle(environ, start_response, *args, **kwds):
            output = handler(environ, start_response, *args, **kwds)
            environ['tiddlyweb.title'] = title
            return output

        return _entitle

    return entangle


def do_html():
    """
    Decorator that makes sure we are sending text/html.
    """

    def entangle(handler):

        def _do_html(environ, start_response, *args, **kwds):
            output = handler(environ, start_response, *args, **kwds)
            start_response('200 OK', [
                ('Content-Type', 'text/html; charset=UTF-8')])
            return output

        return _do_html

    return entangle


def require_role(role):
    """
    Decorator that requires the current user has role <role>.
    """
    try:
        role = unicode(role)
    except NameError:
        pass

    def entangle(handler):

        def _require_role(environ, start_response, *args, **kwds):
            try:
                roles = environ['tiddlyweb.usersign']['roles']
            except KeyError:
                raise UserRequiredError('insufficient permissions')
            if role in roles:
                return handler(environ, start_response, *args, **kwds)
            else:
                raise UserRequiredError('insufficient permissions')

        return _require_role

    return entangle


def require_any_user():
    """
    Decorator that requires the current user be someone other than 'GUEST'.
    """

    def entangle(handler):

        def _require_any_user(environ, start_response, *args, **kwds):
            try:
                username = environ['tiddlyweb.usersign']['name']
            except KeyError:
                raise UserRequiredError('user must be logged in')
                
            if username == 'GUEST':
                raise UserRequiredError('user must be logged in')
            else:
                return handler(environ, start_response, *args, **kwds)

        return _require_any_user

    return entangle


def ensure_bag(bag_name, store, policy_dict=None, description='', owner=None):
    """
    Ensure that bag with name bag_name exists in store.
    If not, create it with owner, policy and description optionally
    provided. In either case return the bag object.
    """
    if policy_dict is None:
        policy_dict = {}
    bag = Bag(bag_name)

    try:
        bag = store.get(bag)
    except NoBagError:
        bag.desc = description
        if owner:
            bag.policy.owner = owner
            bag.policy.manage = [owner]
        for key in policy_dict:
            bag.policy.__setattr__(key, policy_dict[key])
        store.put(bag)

    return bag


def replace_handler(selector, path, new_handler):
    """
    Replace an existing path handler in the selector
    map with a new handler. Usually we want to add a
    new one, but sometimes we just want to replace.
    This makes replacing easy. Courtesy of arno,
    the selector author.
    """
    for index, (regex, _) in enumerate(selector.mappings):
        if regex.match(path) is not None:
            selector.mappings[index] = (regex, new_handler)


def map_to_tiddler(selector, path, bag=None, recipe=None):
    """
    Map the route given in path to the default routing for
    getting, putting and deleting a tiddler. The provided bag
    or recipe name is used to disambiguate the mapping.

    The path must include {tiddler_name} in it somewhere. Examples:

       /{tiddler_name}
       /people/{tiddler_name}
       /a/long/path/to/something/{tiddler_name}
       /{tiddler_name}/something/here
    """
    from tiddlyweb.web.handler.tiddler import get, put, delete

    def handler(environ, start_response):
        if bag:
            environ['wsgiorg.routing_args'][1]['bag_name'] = bag
        elif recipe:
            environ['wsgiorg.routing_args'][1]['recipe_name'] = recipe
        else:
            return selector.not_found(environ, start_response)
        if environ['REQUEST_METHOD'] == 'GET':
            return get(environ, start_response)
        elif environ['REQUEST_METHOD'] == 'PUT':
            return put(environ, start_response)
        elif environ['REQUEST_METHOD'] == 'DELETE':
            return delete(environ, start_response)
        else:
            return selector.method_not_allowed(environ, start_response)

    selector.add(path, GET=handler, PUT=handler, DELETE=handler)


def remove_handler(selector, path):
    """
    Remove an existing path handler in the selector
    map. This disables that route, and will cause a
    404 to be returned for that path.
    """
    for index, (regex, _) in enumerate(selector.mappings):
        if regex.match(path) is not None:
            del selector.mappings[index]


def get_store(config):
    """
    Given the config, return a reference to the store.
    """
    from tiddlyweb.store import Store
    return Store(config['server_store'][0],
            config['server_store'][1],
            {'tiddlyweb.config': config})


def resource_filename(package_name, resource_path):
    """
    simple replacement for resource_filename when pkg_resources is not
    available assumes package is available in the current working directory

    This is required primarily on Google App Engine.

    resource_path is a Unix-style relative file path (using forward slashes)
    """
    return os.path.join(package_name, *resource_path.split("/"))
