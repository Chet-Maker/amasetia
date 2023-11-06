from API.amasetia_app import app
from flask_cors import CORS

# Now apply CORS to the imported app
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
