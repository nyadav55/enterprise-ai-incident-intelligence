# pgAdmin Docker container is exposed on port 5050.
# Step 1: Open pgAdmin
# In PGADMIN(browser) If EAII PostgreSQL is not listed
# You need to register it first:
1. Right-click Servers.
2. Select Register → Server.
3. Under General, enter:
    Name: EAII PostgreSQL
4. Open the Connection tab and enter:
# Field	Value
Host name/address	host.docker.internal
Port	5432
Maintenance database	eaiirp_db
Username	eaiirp_user
Password	eaiirp_dev_password

# Verify the database tables
# Once connected, navigate to:
Servers → EAII PostgreSQL → Databases → eaiirp_db → Schemas → public → Tables
# You should find:
- incidents
- alembic_version