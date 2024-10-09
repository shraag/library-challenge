from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# Load configurations
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Initialize JWTManager

from modules.library.routes import auth_bp, librarian_bp, member_bp
# Register Blueprints (to separate routes into modules)
app.register_blueprint(auth_bp, url_prefix=Config.URL_BASE_PATH+'/auth')  # Authentication routes
app.register_blueprint(librarian_bp, url_prefix=Config.URL_BASE_PATH+'/librarian')  # Librarian actions
app.register_blueprint(member_bp, url_prefix=Config.URL_BASE_PATH+'/member')  # Member actions

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

# Run the application
# if __name__ == '__main__':
#     app.run(debug=True)