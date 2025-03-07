# Interior Design Portfolio Website

A modern portfolio website for an interior design business with a Flask backend and MySQL database.

## Features

- Responsive design
- Contact form with validation
- Portfolio showcase
- Admin interface for managing contacts
- MySQL database integration

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- Node.js (for development)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd interior-design-portfolio
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```sql
CREATE DATABASE interior_design;
```

5. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the database credentials and secret key in `.env`

6. Run the Flask application:
```bash
python app.py
```

7. Access the website:
- Frontend: http://localhost:5000
- Admin API: http://localhost:5000/admin/contacts

## Project Structure

```
interior-design-portfolio/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── portfolio.html
│   └── contact.html
├── app.py
├── requirements.txt
└── .env
```

## API Endpoints

- POST `/contact` - Submit contact form
- GET `/admin/contacts` - Get all contact submissions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 