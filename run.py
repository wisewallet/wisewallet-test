import os

from app import create_app

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)


if __name__ == '__main__':
    app.run("127.0.0.1",5000)
