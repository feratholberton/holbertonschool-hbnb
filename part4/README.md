# HBnB - Business Logic & API Layer

This project is Part 2 of the HBnB application, focusing on the implementation of the core business logic and RESTful API endpoints using Python and Flask. It follows a modular architecture and includes an in-memory persistence layer, which will later be replaced by a database in future phases.

## 📁 Project Structure

```text
hbnb/
├── app/
│   ├── __init__.py                # Flask app factory setup
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py           # User-related API endpoints
│   │       ├── places.py          # Place-related API endpoints
│   │       ├── reviews.py         # Review-related API endpoints
│   │       └── amenities.py       # Amenity-related API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User class definition
│   │   ├── place.py               # Place class definition
│   │   ├── review.py              # Review class definition
│   │   └── amenity.py             # Amenity class definition
│   ├── services/
│   │   ├── __init__.py            # Singleton facade instance
│   │   └── facade.py              # Facade class for layer integration
│   └── persistence/
│       ├── __init__.py
│       └── repository.py          # In-memory repository and interface
├── run.py                         # Entry point to start the Flask app
├── config.py                      # App configuration settings
├── requirements.txt               # Python dependencies
└── README.md                      # This documentation file
```

## 🧰 Installation & Usage

1. Clone the Repository
```bash
git clone https://github.com/feratholberton/holbertonschool-hbnb.git
```

2. Create a Virtual Environment and activate it
Go to part2 dir
```bash
python3 -m venv .venv
. .venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the Application
```bash
python3 run.py
```

5. Local URL
```bash
http://localhost:5000/api/v1/
```
