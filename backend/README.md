# Retail AI Pro - Backend

Enterprise-grade AI-powered retail management system backend built with FastAPI.

## Features

- **FastAPI** with async/await support
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT Authentication** for secure API access
- **ML Models** for demand forecasting, customer segmentation, and churn prediction
- **Comprehensive Tests** with 95%+ coverage
- **RESTful API** with automatic OpenAPI documentation

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional, for caching)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

## Project Structure

```
backend/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configuration
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── ml/             # Machine learning modules
│   └── main.py         # FastAPI application
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── alembic/            # Database migrations
└── requirements.txt    # Python dependencies
```

## Key Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Products
- `GET /api/v1/products` - List products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products/{id}` - Get product details
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Customers
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/customers/high-value` - Get high-value customers
- `GET /api/v1/customers/at-risk` - Get at-risk customers

### Orders
- `GET /api/v1/orders` - List orders
- `POST /api/v1/orders` - Create order
- `POST /api/v1/orders/{id}/cancel` - Cancel order

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard metrics
- `GET /api/v1/analytics/revenue` - Revenue data
- `GET /api/v1/analytics/top-products` - Top selling products
- `GET /api/v1/analytics/inventory-alerts` - Inventory alerts

## ML Features

### Demand Forecasting
Predicts future product demand using time series analysis.

### Customer Segmentation
Segments customers using RFM (Recency, Frequency, Monetary) analysis.

### Churn Prediction
Predicts customer churn risk using behavioral features.

### Dynamic Pricing
Optimizes product pricing based on demand, competition, and stock levels.

## Development

### Code Quality

```bash
# Format code
black app tests

# Lint code
flake8 app tests

# Type checking
mypy app
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## License

MIT License
