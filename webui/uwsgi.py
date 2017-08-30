"""module with flask application instance. used to run a dev server
or for export a WSGI application to external WSGI web server"""
from app import create_app

application = create_app()

if __name__ == '__main__':
    # run dev server is ran with python executable
    application.run(host='127.0.0.1', port=8080, debug=True)
