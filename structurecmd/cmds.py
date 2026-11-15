# Phase 1: Backend Foundation
# Incident Management API

# Create versioned API and repository folders
from sys import ps1


mkdir app\api\v1 -Force
mkdir app\repositories -Force

# Create Python package files
New-Item app\api\v1\__init__.py -ItemType File -Force
New-Item app\repositories\__init__.py -ItemType File -Force

# Create incident implementation files
New-Item app\schemas\incident.py -ItemType File -Force
New-Item app\repositories\incident_repository.py -ItemType File -Force
New-Item app\services\incident_service.py -ItemType File -Force
New-Item app\api\v1\incidents.py -ItemType File -Force
New-Item tests\unit\test_incidents.py -ItemType File -Force

# PostgreSQL Database Integration
# Check Docker installation
docker --version

# Check whether Docker is running
docker ps

# Check your active Python environment
python -c "import sys; print(sys.executable)"

# Check current Git status
git status

# Install Python dependencies
python -m pip install sqlalchemy alembic "psycopg[binary]" python-dotenv

# Start PostgreSQL
docker run --name eaiirp-postgres `
  -e POSTGRES_USER=eaiirp_user `
  -e POSTGRES_PASSWORD=eaiirp_dev_password `
  -e POSTGRES_DB=eaiirp_db `
  -p 5432:5432 `
  -d postgres:16

# to check any status - docker ps
# to check DB rediness - docker exec eaiirp-postgres pg_isready -U eaiirp_user -d eaiirp_db
# install Py DB package - python -m pip install sqlalchemy alembic "psycopg[binary]" python-dotenv
# to verify - python -m pip show sqlalchemy alembic psycopg python-dotenv
# to verify sqlalchemy & others  - python -c "import sqlalchemy, alembic, psycopg, dotenv; print('Database dependencies OK')"

# Run this dependency check:
(.venv) PS E:\git_ny_project\enterprise-ai-incident-intelligence> python -c "import sqlalchemy, alembic, psycopg, dotenv, fastapi; print('All dependencies are available')"
op- All dependencies are available
# Now verify the database connection:
(.venv) PS E:\git_ny_project\enterprise-ai-incident-intelligence> python -c "from sqlalchemy import text; from app.core.database import engine; print(engine.connect().execute(text('SELECT 1')).scalar())"
op - 1

#docker cmd
docker ps
to stop - docker stop ecommerce-pgadmin xyz
to start - docker start ecommerce-pgadmin