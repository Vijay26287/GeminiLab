# ✈️ Personal Trip & Expense Manager

A conversational AI travel companion built with the **Google Agent Development Kit (ADK)** and deployed on **Vertex AI Reasoning Engine (Agent Runtime)**. 

Personal Trip Manager helps travelers manage past and upcoming trips, log expenses across categories (travel, stay, tickets, meals, shopping), convert live foreign currencies, check destination weather & attractions, and remember dietary restrictions and allergies across sessions.

---

## 🏗️ Architecture & Project Structure

```
personal-trip-manager/
├── app/                        # Core ADK Agent Code
│   ├── __init__.py
│   ├── agent.py                # Agent definition, A2UI system prompt & callbacks
│   ├── a2ui_utils.py           # A2UI response formatter callback for ADK Web
│   ├── currency_tools.py       # Foreign currency conversion tool
│   ├── firestore_tools.py      # Firestore database CRUD function tools
│   └── weather_tools.py       # Live weather forecast & attractions tool
├── frontend/                   # Custom Web Frontend
│   ├── main.py                 # FastAPI proxy connecting browser to Agent Engine over A2A
│   ├── requirements.txt        # Frontend dependencies
│   └── static/
│       └── index.html          # Plain HTML/JS Chat UI with native A2UI card renderer
├── scripts/
│   └── seed_firestore.py       # Database seeding script for Firestore
├── pyproject.toml              # Python project configuration & dependencies
└── agents-cli-manifest.yaml    # agents-cli deployment configuration
```

---

## ✨ Features

- **📊 Firestore Database Integration**: Full CRUD operations for `trips` and `expenses` collections.
- **🧠 Vertex AI Memory Bank**: Preserves user allergies (e.g. food, medical) and travel preferences across chat sessions.
- **🌤️ Live Weather & Attractions**: Fetches real-time temperatures, 5-day precipitation forecasts, and curated landmarks via Open-Meteo APIs.
- **💱 Real-Time Currency Conversion**: Converts expenses between local currencies (EUR, JPY, GBP) and USD via Frankfurter / ExchangeRate APIs.
- **🎴 Rich A2UI Interface**: Emits structured A2UI v0.8 cards, tables, and lists.
- **📦 Public Cloud Storage**: Configured Cloud Storage bucket (`gs://personal-trip-manager-assets-qwiklabs-gcp-01-f642bd17f85e`) for hosting trip assets.

---

## ⚡ Quickstart

### 1. Local Testing with `agents-cli`

```bash
# Navigate to project directory
cd /config/Desktop/Session1/personal-trip-manager

# Install dependencies
agents-cli install

# Run agent in CLI mode
agents-cli run "What is the expense breakdown for my Paris getaway?"

# Start ADK Web Playground
agents-cli playground --host 0.0.0.0
```

### 2. Running the Custom Frontend

```bash
cd /config/Desktop/Session1/personal-trip-manager

# Set deployment resource env vars
export AGENT_ENGINE_RESOURCE_NAME="projects/369235135473/locations/us-east1/reasoningEngines/5019193614983495680"
export AGENT_DIRECTORY="app"

# Start FastAPI frontend server
uv run python frontend/main.py
```
Open `http://localhost:8080` in your web browser.

---

## ☁️ Deployment

Deploy to Vertex AI Reasoning Engine (Agent Runtime):

```bash
agents-cli deploy --no-confirm-project
```

- **GCP Project**: `qwiklabs-gcp-01-f642bd17f85e`
- **Region**: `us-east1`
- **Reasoning Engine ID**: `projects/369235135473/locations/us-east1/reasoningEngines/5019193614983495680`
