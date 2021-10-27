from werkzeug.serving import run_simple

from server import app

if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)
