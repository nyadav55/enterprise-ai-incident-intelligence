# ecommerce-pgadmin is the Docker container that runs the pgAdmin application (database management UI).
# - eaiirp-postgres: Stores your EAII database.
# - ecommerce-pgadmin: Provides the browser interface to view tables, run SQL queries, and manage PostgreSQL.
# If you stop ecommerce-pgadmin, your database continues working, but pgAdmin at localhost:5050 becomes unavailable.
docker start ecommerce-pgadmin


# pgAdmin Docker container is exposed on port 5050.
# Step 1: Open pgAdmin
# In PGADMIN(browser) If EAII PostgreSQL is not listed
# You need to register it first:
1. Right-click Servers. 2. Select Register → Server. 3. Under General, enter: Name: EAII PostgreSQL
4. Open the Connection tab and enter:
Host name/address -	host.docker.internal
Port -	5432
Maintenance database -	eaiirp_db
Username -	eaiirp_user
Password -	eaiirp_dev_password

# Verify the database tables
# Once connected, navigate to:
Servers → EAII PostgreSQL → Databases → eaiirp_db → Schemas → public → Tables
# You should find:
- incidents
- alembic_version

# Run migration
$env:DATABASE_URL="postgresql+psycopg://eaiirp_user:eaiirp_dev_password@localhost:5432/eaiirp_test_db"
python -m alembic upgrade head
verfy - docker exec eaiirp-postgres psql -U eaiirp_user -d eaiirp_test_db -c "\dt"

# Why are we running migrations?
Think of it this way:
- SQLAlchemy model: Defines the database table structure in Python.
- Alembic migration: Applies that structure to PostgreSQL.
- Database: Stores the actual tables and data.
We already created eaiirp_test_db, but it has no tables. Migration applies the existing table definitions to this test database.
# Our goal: Run automated tests against eaiirp_test_db, keeping your main eaiirp_db data separate and safe.