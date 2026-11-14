# Phase 1: Backend Foundation
# Incident Management API

# Create versioned API and repository folders
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