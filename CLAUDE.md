# CLAUDE.md
# I experimenten with Claude Code, I'm not using it at the moment 07/09/2025

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Health Hub is a FastAPI-based health tracking application that ingests data from multiple sources (FitNotes, Loop Habits, Strava, Obsidian journals, weather) and provides unified insights through date-based indexing. The project uses SQLAlchemy models with Alembic migrations and SQLite as the database.

## Development Commands

### Environment Setup
- Uses Poetry for dependency management with Python 3.13+
- Create `.env` file for environment variables (DATABASE_URL defaults to `sqlite:///./health_hub.db`)

### Core Commands
```bash
# Install dependencies
poetry install

# Database migrations
poetry run alembic revision --autogenerate -m "description" 
poetry run alembic upgrade head

# Run development server
poetry run uvicorn health_hub.main:app --reload

# Access API documentation
# Visit http://127.0.0.1:8000/docs for Swagger UI
```

### Data Scripts
```bash
# Load FitNotes CSV data
python health_hub/scripts/load_fitnotes_csv.py health_hub/scripts/fitnotes.csv

# Clean existing data
python health_hub/scripts/clean_healthhub_data.py
```

## Architecture

### Core Structure
- `health_hub/main.py` - FastAPI app with router registration
- `health_hub/db.py` - SQLAlchemy database configuration with session management
- `health_hub/models.py` - Database models (ResistanceSet, CardioSession)
- `health_hub/routers/` - API endpoints organized by domain (resistance.py, cardio.py)
- `health_hub/scripts/` - Data ingestion and maintenance scripts

### Database Models
- **ResistanceSet**: Tracks weight training (date, exercise, category, weight, reps)
- **CardioSession**: Tracks cardio activities (date, exercise, category, distance, time)
- All models use date-based indexing for temporal correlation analysis

### API Patterns
- RESTful endpoints with CRUD operations
- Pydantic models for request/response validation (Base, Create, Read schemas)
- SQLAlchemy ORM with dependency injection for database sessions
- Router prefix pattern: `/api/{domain}` (e.g., `/api/resistance`)

### Data Integration Strategy
The application follows a three-phase approach:
1. **Data ingestion** from multiple tracking sources
2. **Normalization and integration** centered around date indexing  
3. **Insight generation** through trend analysis and correlations

Current data sources include FitNotes CSV exports, Loop Habits SQLite backups, with planned integrations for Strava API, Obsidian markdown journals, and weather APIs.