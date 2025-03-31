# Post API - FastAPI Application

A FastAPI-based API for managing user posts with async capabilities and following MVC and other design patterns.

## Features

- User authentication with JWT tokens
- Post creation, retrieval, and deletion
- Caching for post retrieval
- Field validation with Pydantic
- MySQL database integration with SQLAlchemy ORM
- Async database operations support
- Clean architecture with various design patterns

## Design Patterns

The application implements several design patterns:

1. **MVC Pattern**:

   - Models: SQLAlchemy models in `app/api/models/`
   - Views: FastAPI routes in `app/api/routes/`
   - Controllers: Service layer in `app/api/services/`

2. **Repository Pattern**:

   - Abstracts data access operations
   - Implemented in `app/api/repositories/`

3. **Unit of Work Pattern**:

   - Manages database transactions
   - Implemented in `app/api/utils/unit_of_work.py`

4. **Strategy Pattern**:

   - Allows switching between sync and async operations
   - Implemented in `app/api/services/base.py`

5. **Dependency Injection**:
   - Using FastAPI's dependency system
   - Implemented in `app/api/dependencies/`

## Project Structure

```
app/
├── api/
│   ├── dependencies/       # Dependency injection classes
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Repository pattern implementation
│   ├── routes/             # API routes (controllers in MVC)
│   ├── schemas/            # Pydantic models for validation
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── main.py                 # Application entry point
```

## Prerequisites

- Python 3.8+
- MySQL database

## Setup

1. Clone the repository:

```bash
git clone https://github.com/AbrehamGebremedhin/post_api.git
cd post-api
```

2. Create a virtual environment:

```bash
python -m venv .venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the environment variables in `.env`:

```
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/post_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

- `POST /api/auth/signup`: Register a new user
- `POST /api/auth/login`: Login and get access token

### Posts

- `POST /api/posts/`: Create a new post
- `GET /api/posts/`: Get all posts for the authenticated user
- `DELETE /api/posts/{post_id}`: Delete a post
