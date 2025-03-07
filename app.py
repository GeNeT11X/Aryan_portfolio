from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

# Enable CORS
CORS(app)

# Database Configuration
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'interior_design')

# Using PyMySQL as MySQL client for compatibility
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secure-secret-key')

# Initialize database
db = SQLAlchemy(app)

# Contact form model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'service': self.service,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

@app.route('/')
def serve_static():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({'error': 'Error serving static files'}), 500

@app.route('/contact', methods=['POST'])
def contact():
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'service', 'message']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Create new contact entry
        new_contact = Contact(
            name=data['name'].strip(),
            email=data['email'].lower().strip(),
            phone=data.get('phone', '').strip(),
            service=data['service'],
            message=data['message'].strip()
        )
        
        # Save to database
        db.session.add(new_contact)
        db.session.commit()
        
        logger.info(f"New contact form submission from {new_contact.email}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'contact': new_contact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while saving your message.',
            'error': str(e)
        }), 500

@app.route('/admin/contacts', methods=['GET'])
def get_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify({
            'success': True,
            'contacts': [contact.to_dict() for contact in contacts]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching contacts.',
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(HTTPException)
def handle_exception(e):
    logger.error(f"HTTP Exception: {str(e)}")
    return jsonify({
        'success': False,
        'message': str(e),
        'code': e.code
    }), e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    logger.error(f"Unexpected error: {str(e)}")
    return jsonify({
        'success': False,
        'message': 'An unexpected error occurred.',
        'error': str(e)
    }), 500

if __name__ == '__main__':
    app.run(debug=True)
