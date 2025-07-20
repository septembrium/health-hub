# Health Hub

## 🎯 Why

Health Hub aims to provide insights based on correlations, patterns, and predictive analysis from a combined dataset of personal tracking sources.

The ultimate goal is to enable **meaningful, positive behavioral change** by helping the user understand their habits, performance, and mindset over time.

---

## 🛠️ What

The project is structured in **three phases**:

1. **Data ingestion** from multiple sources
2. **Normalization and integration**, centered around the **date**
3. **Insight generation**, including trends, comparisons, and reflective prompts

_Note: Full feature analysis is tracked elsewhere; this README only provides a high-level overview._

---

## ⚙️ How

We're collecting and integrating data from the following sources:

- 🏋️ [`FitNotes`](https://www.fitnotesapp.com/) — CSV export for strength & cardio workouts
- 🔁 [`Loop Habits Tracker`](https://loophabits.org/) — SQLite `.db` from backup zip
- 🚴 [`Strava`](https://strava.com) — via API or data export
- 📝 [`Obsidian`](https://obsidian.md/) — markdown-based daily & weekly journals
- 🌦️ Weather — via API (planned)

All data is unified via **date-based indexing**, stored in a simple [SQLite](https://www.sqlite.org/) database, and served via [FastAPI](https://fastapi.tiangolo.com/). Additional tooling includes Alembic for migrations and Pandas for data analysis.

---

## 📦 Top-Level Dependencies

These are the main packages used in the backend:

- `fastapi` – high-performance web API framework
- `uvicorn` – ASGI server for running FastAPI
- `sqlalchemy` – ORM for defining and querying DB models
- `alembic` – database schema versioning/migrations
- `python-dotenv` – load environment variables from `.env` files
- `pydantic` – data validation using Python type hints
- `pandas` – for CSV parsing, analysis, and time-series operations

---

## 🧩 Data Sources Overview

Health Hub integrates both structured and unstructured data to create a unified timeline for analysis.

### 📊 Structured / External Data

#### 🏋️ FitNotes (CSV)
- **Format:** CSV export
- **Content:** Resistance training (sets, reps, weight), cardio sessions (duration, distance)
- **Use:** Track volume, PRs, frequency, performance trends

#### 🚴 Strava (API or Export)
- **Format:** API or JSON export
- **Content:** Cardio metrics (heart rate, pace, distance, elevation)
- **Use:** Analyze endurance trends; correlate with habits or journal reflections

#### 🌦️ Weather (API)
- **Format:** OpenWeather or Meteostat API
- **Content:** Temperature, rain, wind, etc.
- **Use:** Assess environmental effects on training, energy, and mood

---

### 📝 Unstructured / Reflective Data

#### 📓 Obsidian Journals (Markdown)
- **Format:** `.md` files (daily/weekly)
- **Content:** Reflections, productivity notes, mood, goals, insights
- **Use:** Surface recurring themes and link mindset to physical outcomes

#### 🔁 Habits Loop (SQLite)
- **Format:** SQLite `.db`
- **Content:** Daily habit tracking (e.g., sleep, alcohol, meditation)
- **Use:** Identify behavioral patterns and habit-performance correlations

---

Each data source is indexed by date and used to generate timelines, comparisons, and actionable insights to support self-awareness and goal alignment.

---
## 🚀 How to Run
Make sure you're using Python 3.13 and have [Poetry](https://python-poetry.org/) installed. Make a .env file based on the example in the root.

   ```bash
    poetry install
    poetry run alembic revision --autogenerate -m "init"
    poetry run alembic upgrade head
    poetry run uvicorn health_hub.main:app --reload
   ```

Visit http://127.0.0.1:8000/docs for the interactive Swagger UI.

I've kept the .vscode/launch.json in this repository, those are the launchers I use to run in development. If this file every get's stale (very likely you'll find hints in that file for sure).

## 🪪 License

This project is licensed under the [Creative Commons Attribution 4.0 License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You’re free to use it however you like — just give credit by mentioning **Bert Heymans / @bertheymans** in your README, dashboard, or wherever it makes sense.

# Now that you've read all the way to here, I might as well throw in a bit of poerty
49.
"Birds find rest, in narrow nest
When weary of their wingèd quest;
Beasts find fare, in woody lair
When storm and snow are in the air."

-- a bit from Percy Bysshe Shelley's The Mask of Anarchy


