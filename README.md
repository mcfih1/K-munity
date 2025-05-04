# K-munity - Social Impact Platform

K-munity is a social impact platform that connects communities through local food bank assistance, disaster relief coordination, and youth mentorship programs.

## Features

- User authentication and authorization
- Local food bank assistance requests
- Disaster relief coordination
- Youth mentorship programs
- Community events management
- Secure payment processing
- VIP membership system

## Tech Stack

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Stripe Payment Processing

### Frontend (Coming Soon)
- React
- Material-UI
- Redux
- Axios

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- Node.js and npm (for frontend)
- Stripe account

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/k-munity.git
cd k-munity/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp env.example .env
```
Edit the `.env` file with your configuration values.

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the development server:
```bash
flask run
```

The API will be available at `http://localhost:5000`

### Frontend Setup (Coming Soon)

## API Documentation

### Authentication
- POST `/api/auth/register` - Register a new user
- POST `/api/auth/login` - Login and get JWT token

### Requests
- POST `/api/requests` - Create a new request
- GET `/api/requests` - Get all requests (filterable by type)

### Donations
- POST `/api/donations` - Process a donation

### Events
- POST `/api/events` - Create a new event
- GET `/api/events` - Get all events (filterable by type)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please contact support@k-munity.com 