from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

# Load configurations
app.config.from_object(Config)

CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Initialize JWTManager

# Register Blueprints (to separate routes into modules)
from modules.library.routes import librarian_bp
app.register_blueprint(librarian_bp, url_prefix=Config.URL_BASE_PATH+'/librarian')  # Librarian actions

from modules.library.routes import member_bp
app.register_blueprint(member_bp, url_prefix=Config.URL_BASE_PATH+'/member')  # Member actions

from modules.library.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix=Config.URL_BASE_PATH+'/auth')  # Authentication actions

# Default route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Library Management System"}), 200

# Error handler for 404 - Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

# Error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)