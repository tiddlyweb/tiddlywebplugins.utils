def test_compile():
    try:
        import tiddlywebplugins.utils
        assert True
    except ImportError as exc:
        assert False, exc
