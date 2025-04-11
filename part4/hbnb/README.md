# 🏠 HBNB - Holberton Bed & Breakfast

<div align="center">
  <img src="images/logo.png" alt="HBNB Logo" width="250">
  <p><em>A complete accommodation booking platform</em></p>
  <hr>
</div>

## 📋 Table of Contents

- [🔍 Overview](#-overview)
- [📂 Project Structure](#-project-structure)
- [🔄 Project Evolution](#-project-evolution)
- [🏗️ Technical Architecture](#️-technical-architecture)
- [✨ Features](#-features)
- [🛠️ Technologies Used](#️-technologies-used)
- [🚀 Installation & Setup](#-installation--setup)
- [📱 User Guide](#-user-guide)
- [📡 API Reference](#-api-reference)
- [👨‍💻 Development Team](#-development-team)

## 🔍 Overview

HBNB (Holberton Bed & Breakfast) is a complete web application inspired by AirBnB, developed as part of the Holberton School curriculum. This project is the result of progressive development through four parts, from initial design to a functional web application allowing users to browse accommodations, view their details, and submit reviews.

This version (Part 4) represents the culmination of the project with the integration of a user interface with the backend developed in the previous phases.

## 📂 Project Structure

The HBNB project (Part 4) is organized as follows:

```
hbnb/
├── ER_diagrams/              # Entity-relationship diagrams
├── app/                      # Main application
│   ├── __init__.py
│   ├── api/                  # REST API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py      # User endpoints
│   │       ├── places.py     # Place endpoints
│   │       ├── reviews.py    # Review endpoints
│   │       └── amenities.py  # Amenity endpoints
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── base_model.py    # Base class for all models
│   │   ├── user.py          # User model
│   │   ├── place.py         # Place model
│   │   ├── review.py        # Review model
│   │   └── amenity.py       # Amenity model
│   └── services/            # Business services
│       ├── __init__.py
│       └── facade.py        # Facade pattern implementation
├── database/                # Database scripts and migrations
├── images/                  # Frontend graphic resources
├── tests/                   # Unit and integration tests
├── *.html                   # User interface HTML pages
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   └── place.html           # Place detail page
├── scripts.js               # Frontend JavaScript code
├── styles.css               # CSS styles
├── config.py                # Application configuration
├── requirements.txt         # Python dependencies
└── run.py                   # Application entry point
```

## 🔄 Project Evolution

The HBNB project was developed in four distinct phases, each adding a new layer of functionality:

### Part 1: Documentation and Design 📝
- Detailed technical documentation
- UML diagrams (classes, sequences)
- API specifications
- Architecture planning

### Part 2: Backend API 🔌
- REST API implementation with Flask
- Data models creation
- Layered structure (API, services, models)
- Unit and integration testing
- In-memory storage (no persistence)

### Part 3: Data Persistence 💾
- SQLAlchemy ORM integration
- Database configuration
- Alembic migrations
- ER diagrams
- Database testing

### Part 4: Frontend User Interface 🖥️
- Static HTML pages
- JavaScript for dynamic interactions
- CSS for layout and animations
- Complete integration with backend API
- Smooth user experience

## 🏗️ Technical Architecture

HBNB is built on a layered architecture that clearly separates responsibilities:

### Presentation Layer 🎨
- Static HTML pages
- JavaScript for API interaction
- CSS for styling and layout

### API Layer 🔗
- RESTful endpoints exposed by Flask
- Request validation
- Authentication and authorization
- Response formatting

### Service Layer ⚙️
- Facade pattern application
- Business operations orchestration
- Business rules validation
- Coordination between API and models

### Model Layer 📊
- Domain entities with attributes and behaviors
- Entity-level data validation
- Entity relationships (user-place, place-review)
- ORM mapping with SQLAlchemy

### Persistence Layer 💽
- Database access via SQLAlchemy
- SQLite storage (development)
- PostgreSQL support (production)
- Schema migrations with Alembic

## ✨ Features

### User Interface 🖱️
- Smooth navigation between pages
- Available accommodation catalog
- Price filtering
- Detailed accommodation viewing
- Star rating system

### Authentication 🔐
- User registration and login
- JWT tokens for API authentication
- Role-based access control

### Accommodation Management 🏘️
- Display of accommodation list
- Accommodation details (description, price, amenities)
- Intuitive navigation

### Review System ⭐
- Review submission with text and rating
- Display of reviews by accommodation
- Average rating by accommodation

## 🛠️ Technologies Used

### Frontend 🌐
- HTML5 for page structure
- CSS3 for styling and animations
- JavaScript (ES6+) for interactivity
- Fetch API for asynchronous calls

### Backend 🧠
- Python 3.8+ as the main language
- Flask as the web framework
- SQLAlchemy as ORM
- JWT for authentication

### Database 🗄️
- SQLite in development
- PostgreSQL in production

### Development Tools 🔧
- Git for versioning
- pytest for testing
- curl for manual API testing

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Modern web browser

### Installation

1. Clone the repository and navigate to the project folder
```bash
git clone https://github.com/your-name/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4/hbnb
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure the environment (optional - use default values for development)
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

### Running the Backend API

5. Initialize the database
```bash
flask db upgrade
```

6. Run the backend server
```bash
python run.py
```

7. Access the API documentation at `http://localhost:5000/api/v1` (Swagger UI)

### Running the Frontend

8. In a separate terminal, start the HTTP server for the frontend
```bash
python3 -m http.server 8080
```

9. Access the application in your browser: `http://localhost:8080`

## 📱 User Guide

### Home Page (index.html)
- List of available accommodations
- Filter by maximum price
- Navigate to accommodation details

### Detail Page (place.html)
- Detailed information about an accommodation
- List of reviews
- Ability to add a review (logged-in user)

### Login (login.html)
- Login form
- Redirect to home page after login

## 📡 API Reference

The HBNB API is accessible via the `/api/v1` prefix and offers the following endpoints:

### Users 👤

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authentication |
| GET | `/users` | List of users |
| GET | `/users/{id}` | User details |
| POST | `/users` | Create a user |
| PUT | `/users/{id}` | Update a user |
| DELETE | `/users/{id}` | Delete a user |

### Places 🏡

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/places` | List of accommodations |
| GET | `/places/{id}` | Accommodation details |
| POST | `/places` | Create an accommodation |
| PUT | `/places/{id}` | Update an accommodation |
| DELETE | `/places/{id}` | Delete an accommodation |

### Reviews 📝

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reviews` | List of reviews |
| GET | `/places/{id}/reviews` | Reviews for an accommodation |
| POST | `/reviews` | Create a review |
| PUT | `/reviews/{id}` | Update a review |
| DELETE | `/reviews/{id}` | Delete a review |

## 👨‍💻 Development Team

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/jbn179">
        <img src="https://github.com/jbn179.png" width="100px;" alt="Benjamin RISTORD"/><br/>
        <sub><b>Benjamin RISTORD</b></sub>
      </a><br/>
    </td>
</table>

---

<div align="center">
  <p>© 2025 - Holberton School</p>
  <p>Developed as part of the Holberton School program</p>
</div>