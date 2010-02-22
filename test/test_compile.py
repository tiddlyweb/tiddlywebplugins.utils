


def test_compile():
    try:
        import tiddlywebplugins.utils
        assert True
    except ImportError, exc:
        assert False, exc
