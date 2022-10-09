import os
import traceback
from multiprocessing import Lock

from flask import Flask
from flask_restful import Api

from .database import db
from .dataset import FetchCSV
from .resources import init_resources

lock = Lock()


def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DEVConfig')
    app.config.from_object(config_type)

    # Configure API
    api = Api(app)

    # Configure Database with SQLAlchemy
    db.init_app(app)

    with app.app_context(), lock:
        print(" * Creating db tables...")
        db.create_all()
        try:
            IRIS_CSV = FetchCSV.download_csv_from_url(app.config["CSV_URL"])
        except Exception as e:
            print(traceback.format_exc())
            print(
                f"Unhandled error while loading CSV from URL: {app.config['CSV_URL']}"
            )

    # Initialize Rest end-points
    init_resources(api)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
