from waitress import serve
from mantenedor.wsgi import application

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=9000)
