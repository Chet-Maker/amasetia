from API.amasetia_app import app
from flask_cors import CORS
import logging

if __name__ == '__main__':
    logging.getLogger('flask_cors').level = logging.DEBUG
    app.run(debug=True)
