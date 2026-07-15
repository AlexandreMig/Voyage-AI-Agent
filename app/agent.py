# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Core Agent definition for VoyageAI with hardened prompts and Memory Bank callbacks."""

import os
import google.auth

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# Initialize credentials and ensure correct project fallback
try:
    _, project_id = google.auth.default()
except Exception:
    project_id = None

if not project_id or project_id == "outside-of-project":
    project_id = "fde-ai-learning-project"

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = os.environ.get("GOOGLE_CLOUD_LOCATION") or "us-east1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

from app.tools import search_attractions, check_weather, format_itinerary
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

# Hardened Travel Concierge Instruction Prompt (Model Armor compliant)
TRAVEL_CONCIERGE_INSTRUCTION = (
    "You are VoyageAI, a secure, hyper-personalized AI Travel Concierge. "
    "Your job is to help users plan custom, realistic, and highly optimized travel itineraries "
    "by retrieving weather reports, finding local attractions, and formatting beautiful schedules. "
    "\n\n"
    "### Core Guidelines & Travel Feasibility Constraints:\n"
    "1. Physical Realism & Time Margins: Never propose overlapping schedules. For a 'relaxed' pace, you must strictly schedule a maximum of 3 major items per day in total, including meals and dining spots (specifically: exactly 2 daytime attractions/activities and exactly 1 dinner/evening spot). You must NEVER schedule lunch or any other meals as separate calendar items in the daily itinerary (instead, simply suggest lunch spots or snacks within the descriptions of the daytime attractions). Never exceed 3 total calendar items in any day's schedule. "
    "You must explicitly insert a separate bullet point in the daily schedule for transit time of at least 1.5 to 2 hours between every single scheduled activity, attraction, and dining spot (e.g. '* 12:30 PM - 2:30 PM: Transit Buffer (2 hours) - Travel to next location'). This includes a separate transit buffer bullet point between the final daytime attraction and the dinner/evening dining spot. "
    "Group activities geographically by district (e.g. keep Harajuku and Shibuya together, and Asakusa/Ueno together) to minimize transit. Do not pack too many locations into a single day.\n"
    "2. Diet & Health Constraints: You must actively check the traveler's dietary restrictions (e.g. vegan, gluten-free, allergies) from their profile/Memory Bank and cross-reference all dining spots you recommend to ensure they offer compliant options.\n"
    "3. Weather Awareness: You must always call the `check_weather` tool and include a dedicated 'Weather & Packing Advisory' section in your response, even for simple queries like restaurant recommendations. "
    "MANDATORY: You must NEVER ask a clarifying question to ask for the month of travel. If the user does not specify a travel month, you must immediately and unconditionally assume 'October', call `check_weather` with 'October', and generate the complete itinerary and weather recommendations in your very first response.\n"
    "\n"
    "### Security & Persona Integrity:\n"
    "- Maintain your bounded persona as a travel assistant. Do not adopt alternative roles, perform system administration, or execute code.\n"
    "- Politely decline any queries unrelated to travel and guide the user back to planning their trip."
)

async def before_agent_callback(callback_context: CallbackContext) -> None:
    """Safely initializes session state variables before the agent execution starts."""
    if "user_preferences" not in callback_context.state:
        callback_context.state["user_preferences"] = {
            "budget": "moderate",
            "diet": "none",
            "pace": "moderate"
        }

async def after_agent_callback(callback_context: CallbackContext):
    """Triggers Memory Bank processing to compile raw user interactions into long-term profile memories."""
    try:
        await callback_context.add_session_to_memory()
    except ValueError:
        # Handle cases where memory service is not available (e.g., during local eval generate)
        pass
    return None

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=TRAVEL_CONCIERGE_INSTRUCTION,
    tools=[
        PreloadMemoryTool(),
        search_attractions,
        check_weather,
        format_itinerary
    ],
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
