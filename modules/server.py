from flask import Flask

from modules.routes import register_routes


def create_server():
    app = Flask(
        __name__,
        static_folder="../frontend",
        static_url_path=""
    )

    register_routes(app)

    return app