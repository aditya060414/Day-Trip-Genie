import os
import sys
import asyncio
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Fix Windows console emoji printing issues
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Ensure Vertex AI is not enabled
os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)
os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
os.environ.pop("GOOGLE_CLOUD_LOCATION", None)

# Load environment variables from .env if present
from dotenv import load_dotenv
load_dotenv()

# Initialize Session Service
session_service = InMemorySessionService()

def create_day_trip_agent():
    return Agent(
        name="day_trip_agent",
        model="gemini-2.5-flash",
        description="Agent specialized in generating spontaneous full-day itineraries based on mood, interests, and budget.",
        instruction="""
        You are the "Spontaneous Day Trip" Generator 🚗 - a specialized AI assistant that creates engaging full-day itineraries.

        Your Mission:
        Transform a simple mood or interest into a complete day-trip adventure with real-time details, while respecting a budget.

        Guidelines:
        1. **Budget-Aware**: Pay close attention to budget hints like 'cheap', 'affordable', or 'splurge'. Use Google Search to find activities (free museums, parks, paid attractions) that match the user's budget.
        2. **Full-Day Structure**: Create morning, afternoon, and evening activities.
        3. **Real-Time Focus**: Search for current operating hours and special events.
        4. **Mood Matching**: Align suggestions with the requested mood (adventurous, relaxing, artsy, etc.).

        RETURN the itinerary structured exactly like this, wrapping each time block in a div with the class "time-box":
        
        <div class="time-box">
        ### 🌅 Morning
        **Venue:** [Name]
        **Details:** [Activities, cost, tips]
        </div>
        
        <div class="time-box">
        ### ☀️ Afternoon
        [Afternoon details]
        </div>
        
        <div class="time-box">
        ### 🌇 Evening
        [Evening details]
        </div>

        <div class="time-box">
        ### 🌙 Night
        [Night details]
        </div>

        Do not wrap your response in ```html or ```markdown blocks. Just return the raw tags and markdown.
        """,
        tools=[google_search]
    )

day_trip_agent = create_day_trip_agent()

# FastAPI App
app = FastAPI(title="Day Trip Genie API")

class GenerateRequest(BaseModel):
    api_key: Optional[str] = None
    query: str

@app.post("/api/generate")
async def generate_itinerary(req: GenerateRequest):
    # Use the provided key from the UI, or fallback to the .env file
    current_key = req.api_key or os.environ.get("GOOGLE_API_KEY")
    
    if not current_key:
        raise HTTPException(status_code=400, detail="API key is required. Paste it in the UI or add it to the .env file.")
        
    # Temporarily set the API key for this request. 
    # Note: Setting os.environ globally in an async web server can cause race conditions 
    # between concurrent requests if users provide different keys.
    os.environ["GOOGLE_API_KEY"] = current_key
    
    # create a new session per request for this demo
    session = await session_service.create_session(
        app_name=day_trip_agent.name,
        user_id="web_user_001"
    )
    
    runner = Runner(
        agent=day_trip_agent,
        session_service=session_service,
        app_name=day_trip_agent.name
    )
    
    final_response = ""
    try:
        print(f"\n Running query for agent: '{day_trip_agent.name}' in session: '{session.id}'...")
        print(f"🗣️ User Query: '{req.query}'")
        async for event in runner.run_async(
            user_id="web_user_001",
            session_id=session.id,
            new_message=Content(parts=[Part(text=req.query)], role="user")
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
    except Exception as e:
        print(f"Error during ADK execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"response": final_response}

# Mount static files and serve index.html at root
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    print("🧞 Starting Day Trip Genie Web Server on http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
