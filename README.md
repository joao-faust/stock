# Stock

Inventory control API built with FastAPI, SQLAlchemy, and Alembic.

The project allows products to be registered, stock to be checked, products to be activated or deactivated, inbound and outbound stock movements to be recorded, and low-stock products to be listed.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- MySQL with PyMySQL

## Requirements

- Python installed
- MySQL running
- Database created

Example database creation:

```sql
CREATE DATABASE stock;
```

## Configuration

Create a `.env` file in the project root with the database and JWT settings:

```env
DB_URL=mysql+pymysql://root:root@localhost/stock
JWT_SECRET=change-me
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=30
```

Install the dependencies:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Migrations

Apply migrations:

```bash
make migrate:up
```

Create a migration:

```bash
make migrate:make NAME="migration_name"
```

Revert the latest migration:

```bash
make migrate:down
```

## Running

```bash
make api:run
```

The interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### Users

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/users/` | Creates a user |
| `PUT` | `/users/` | Updates the authenticated user with password confirmation |
| `DELETE` | `/users/` | Deletes the authenticated user with password confirmation |

### Products

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/products/` | Creates a product |
| `GET` | `/products/` | Lists products |
| `GET` | `/products/low-stock` | Lists low-stock products |
| `GET` | `/products/{id}` | Reads a product by ID |
| `PUT` | `/products/{id}` | Updates a product by ID |
| `PUT` | `/products/{id}/status` | Activates or deactivates a product by ID |
| `DELETE` | `/products/{id}` | Deletes a product by ID |

### Movements

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/movements/` | Creates a stock movement |
| `GET` | `/movements/products/{product_id}` | Lists movements for a product |

## Main Rules

- Products are created with `is_active` set to `true` and their initial quantity is controlled by the model.
- Products with `is_active` set to `false` cannot receive movements.
- Outbound movements cannot leave stock with a negative balance.
- Products with movements cannot be physically deleted.
- Low-stock products are products with `is_active` set to `true` whose current quantity is less than or equal to the minimum stock.

## Structure

```text
app/
  core/           Database configuration, settings, and error handlers
  models/         SQLAlchemy models
  repositories/   Data access through abstract base classes
  routers/        FastAPI routes
  schemas/        Pydantic schemas
  services/       Business rules
migrations/       Alembic migrations
docs/             Requirements documentation
```
