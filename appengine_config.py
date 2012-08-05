from gaesessions import SessionMiddleware


def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app,
        cookie_key="pydaycba_pydaycba2012_pydaycba_pydaycba2012_pydaycba_pydaycba2012",
        cookie_only_threshold=0)
    return app
