import asyncio
import os
import sys

os.environ["GOOGLE_CLOUD_PROJECT"] = "fde-ai-learning-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-east1"

sys.path.append("/Users/alexlopes/.gemini/antigravity/scratch/voyageai")

from app.agent import app as adk_app
from app.agent import root_agent
from google.adk.runners import Runner
from app.app_utils import services
from google.genai import types

def make_message(text: str):
    return types.Content(
        role="user", parts=[types.Part.from_text(text=text)]
    )

async def main():
    session_service = services.get_session_service()
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name=adk_app.name,
    )
    
    session = session_service.create_session_sync(user_id="diagnostic_user", app_name=adk_app.name)
    session_id = session.id
    
    prompt = "Please prepare a relaxed 3-day itinerary for a trip to Tokyo. I'd love to visit Meiji Jingu and Shinjuku Gyoen."
    print(f"QUERY: {prompt}\n")
    
    events = list(runner.run(
        new_message=make_message(prompt),
        user_id="diagnostic_user",
        session_id=session_id
    ))
    
    for ev in events:
        if hasattr(ev, "content") and ev.content:
            print("Content chunk:", ev.content)
        else:
            print("Event:", ev)

if __name__ == "__main__":
    asyncio.run(main())
