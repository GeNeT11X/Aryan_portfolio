from flask import Flask, request, jsonify, render_template
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

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS
CORS(app)

# Database Configuration
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')  # Handle empty passwords properly
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'interior_design')

# Using PyMySQL as MySQL client for compatibility
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
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

# Ensure database connection works before creating tables
try:
    with app.app_context():
        db.session.execute("SELECT 1")  # Test connection
        db.create_all()
        logger.info("Database connection successful & tables created.")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")

# Routes

@app.route('/')
def home():
    """Serve the homepage."""
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    """Serve the portfolio page."""
    return render_template('portfolio.html')

@app.route('/contact')
def contact_page():
    """Serve the contact page."""
    return render_template('contact.html')

@app.route('/contact', methods=['POST'])
def submit_contact():
    """Handles contact form submission."""
    try:
        if not request.is_json:
            return jsonify({'success': False, 'message': 'Content-Type must be application/json'}), 400

        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'service', 'message']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'success': False, 'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

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
        
        return jsonify({'success': True, 'message': 'Thank you! We will get back to you soon.', 'contact': new_contact.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500

@app.route('/admin/contacts', methods=['GET'])
def get_contacts():
    """Fetch all submitted contact messages."""
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify({'success': True, 'contacts': [contact.to_dict() for contact in contacts]}), 200
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500

# Error Handlers

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {str(e)}")
    return jsonify({'success': False, 'message': str(e), 'code': e.code}), e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'success': False, 'message': 'An unexpected error occurred.', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
