# 🏠 HBnB Application

This is the HBnB (AirBnB clone) application, a RESTful API for managing users, places, reviews, and amenities.

## 📁 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

### 📚 Directory and File Descriptions

- `app/`: Contains the core application code.
- `app/api/`: Houses the API endpoints, organized by version.
- `app/models/`: Contains the business logic classes.
- `app/services/`: Implements the Facade pattern for communication between layers.
- `app/persistence/`: Implements the in-memory repository.
- `run.py`: Entry point for running the Flask application.
- `config.py`: Configuration for environment variables and application settings.
- `requirements.txt`: Lists all Python packages needed for the project.

## 🚀 Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part2
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application

To run the application, use the following command:

```bash
python3 run.py
```

The application will start, and you can access the API at `http://localhost:5000`.

## 📖 API Documentation

API documentation will be available at `http://localhost:5000/api/v1/` when the application is running.

## 🧠 Business Logic Layer

The Business Logic layer contains the core entities of the HBnB application. These entities are implemented as Python classes in the `app/models/` directory.

### Entities

1. **BaseModel**: The base class for all entities, providing common attributes and methods.
   - Attributes: id, created_at, updated_at
   - Methods: save(), update(), to_dict()

2. **User**: Represents a user of the HBnB application.
   - Attributes: first_name, last_name, email, is_admin
   - Methods: validate()

3. **Place**: Represents a place that can be rented.
   - Attributes: title, description, price, latitude, longitude, owner, reviews, amenities
   - Methods: validate(), add_review(), add_amenity()

4. **Review**: Represents a review for a place.
   - Attributes: text, rating, place, user
   - Methods: validate()

5. **Amenity**: Represents an amenity that a place can have.
   - Attributes: name
   - Methods: validate()

Each entity class inherits from the BaseModel class and implements its own validation logic and specific methods. The relationships between entities (e.g., User owning Places, Places having Reviews and Amenities) are represented through object references.

This structure allows for easy manipulation of data and enforcement of business rules within the application.
