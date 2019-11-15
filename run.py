import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    if config_name == "development"
        PORT = 6000
    else:
        PORT = 5000
    app.run("127.0.0.1",PORT)
