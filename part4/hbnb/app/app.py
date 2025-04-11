import os
from app import create_app

# Configure environment for Flask development
os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Set CORS environment variables
os.environ['CORS_ALLOWED_ORIGINS'] = '*'
os.environ['CORS_SUPPORTS_CREDENTIALS'] = 'true'

# Create app instance
app = create_app('config.DevelopmentConfig')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
