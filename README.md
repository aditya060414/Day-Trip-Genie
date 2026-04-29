# Day Trip Genie 🧞

![Day Trip Genie Banner](https://via.placeholder.com/800x200/1D9E75/FFFFFF?text=Day+Trip+Genie)

## 📖 Overview
**Day Trip Genie** is an AI-powered travel planner built using the **Google Cloud GenAI Agent Development Kit (ADK)** and **FastAPI**. It takes your starting location, mood, budget, and interests to generate a highly personalized, full-day itinerary.

The agent leverages the `google_search` tool to fetch real-time information (such as opening hours, current events, and practical tips) directly from the web, ensuring the itinerary is accurate and actionable.

---

## 📝 Background
> *Note: This was my 1st session. I have not written the core logic of the agent from scratch, but rather used this project to try to understand its working and how ADK integrates with a web server. The beautiful UI design is referred from Claude.*

---

## 🚀 Key Features
- **Real-Time Web Search**: The ADK agent dynamically searches the web to build your itinerary with up-to-date data.
- **Beautiful UI**: An elegant, responsive web interface with a built-in Dark Mode toggle.
- **Structured Outputs**: Itineraries are structured into distinct, elevated "time-boxes" (Morning, Afternoon, Evening, Night) and rendered cleanly with Markdown via `marked.js`.
- **Secure Backend**: API keys are handled safely via a `.env` file instead of being exposed directly in the frontend HTML.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Google Cloud GenAI ADK
- **Frontend:** Vanilla HTML/CSS/JS, marked.js

---

## 📁 Project Structure
```text
📦 session_1
 ┣ 📂 static
 ┃ ┗ 📜 index.html        # The HTML/JS/CSS frontend interface
 ┣ 📜 app.py              # The FastAPI server & Google ADK Agent configuration
 ┣ 📜 day_trip_agent.py   # Original agent script (kept for reference)
 ┣ 📜 .env                # Secret keys configuration (not committed)
 ┗ 📜 .gitignore          # Git ignore rules
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.9 or higher
- A Google AI Studio API Key (It's free: [Get one here](https://aistudio.google.com/apikey))

### 2. Install Dependencies
Ensure you have the required packages installed in your Python environment:
```bash
pip install fastapi uvicorn python-dotenv google-adk google-generativeai
```

### 3. Configure Your Environment
Create a `.env` file in the root directory (alongside `app.py`) and add your AI Studio API key:
```ini
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Server
Start the FastAPI development server:
```bash
python app.py
```
*(Alternatively, run `uvicorn app:app --host 0.0.0.0 --port 8000 --reload`)*

### 5. Plan Your Trip!
1. Open your browser and navigate to [http://localhost:8000](http://localhost:8000). 
2. Enter your starting location.
3. Select your mood, budget, and a few interests.
4. Click **Plan my day** and watch the ADK build your custom itinerary!