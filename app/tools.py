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

"""Specialized travel planning tools for VoyageAI with robust Pydantic validation."""

import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# ==========================================
# 📋 Pydantic Validation Schemas & Models
# ==========================================

class AttractionItem(BaseModel):
    name: str = Field(..., description="The name of the attraction or restaurant.")
    category: str = Field(..., description="The category, e.g. Garden, Monument, Restaurant.")
    rating: float = Field(..., description="The average review rating (out of 5.0).")
    description: str = Field(..., description="Detailed description of the attraction.")
    hours: str = Field(..., description="Operating hours of the attraction.")
    vegan_friendly: bool = Field(..., description="Whether the attraction is vegan friendly.")

class SearchAttractionsInput(BaseModel):
    location: str = Field(..., description="The destination city to search. Supported cities are 'Tokyo' and 'Paris'.")
    query: str = Field(..., description="The filter query keyword (e.g., 'gardens', 'vegan sushi').")

class SearchAttractionsResponse(BaseModel):
    status: str = Field("success", description="The status of the query.")
    location: str = Field(..., description="The destination searched.")
    attractions: List[AttractionItem] = Field(..., description="List of matching attractions.")

class CheckWeatherInput(BaseModel):
    location: str = Field(..., description="The destination city. Supported cities are 'Tokyo' and 'Paris'.")
    month: str = Field(..., description="The month of travel (e.g. 'October', 'August').")

class CheckWeatherResponse(BaseModel):
    status: str = Field("success", description="The status of the query.")
    location: str = Field(..., description="The destination city.")
    month: str = Field(..., description="The travel month.")
    average_temperature: str = Field(..., description="Average temperature range.")
    conditions_summary: str = Field(..., description="Weather summary description.")
    packing_recommendations: str = Field(..., description="Packing advisory recommendations.")

class ActivityItem(BaseModel):
    time: str = Field(..., description="The scheduled time (e.g., '09:00 AM - 10:30 AM' or 'Transit Buffer (2 hours)').")
    name: str = Field(..., description="The name of the activity or attraction.")
    description: str = Field("", description="Brief description of what to do there.")

class DayItinerary(BaseModel):
    day_title: str = Field(..., description="The title of the day (e.g. 'Day 1: Arrival & Historic Sights').")
    activities: List[ActivityItem] = Field(..., description="The chronological activities for the day.")

class ItineraryDataInput(BaseModel):
    destination: str = Field(..., description="The destination city.")
    duration: str = Field(..., description="The duration of the trip (e.g., '3 Days').")
    days: List[DayItinerary] = Field(..., description="Day-by-day itineraries.")

class ConfirmationRequest(BaseModel):
    action: str = Field(..., description="The action that requires human confirmation.")
    reason: str = Field(..., description="The reason why this action needs explicit confirmation.")


# ==========================================
# 🛠️ Tool Implementations
# ==========================================

def search_attractions(location: str, query: str) -> dict:
    """Searches for localized attractions, landmarks, restaurants, and reviews.

    Args:
        location: The city or area to search in. Supported: "Tokyo", "Paris".
        query: Specific keyword to filter attractions (e.g. "gardens", "vegan sushi").

    Returns:
        A dictionary containing a list of matching attractions with ratings and descriptions.
    """
    # 📝 Intent Logging
    print(f"[INTENT] Tool 'search_attractions' triggered with location='{location}' and query='{query}'")

    try:
        # Explicit Pydantic validation
        inputs = SearchAttractionsInput(location=location, query=query)
    except ValidationError as e:
        # Guided recovery for validation errors
        err_msg = f"Argument validation failed for search_attractions: {e.errors()}"
        print(f"[OUTCOME] Tool failed. {err_msg}")
        return {
            "status": "error",
            "message": "Argument validation failed.",
            "errors": e.errors(),
            "guided_recovery": "Please ensure you pass non-empty string arguments for both 'location' and 'query'. Example: location='Tokyo', query='gardens'."
        }

    loc_lower = inputs.location.lower()
    q_lower = inputs.query.lower()

    # Guided recovery for unsupported locations
    if "tokyo" not in loc_lower and "paris" not in loc_lower:
        rec_msg = f"The database only contains records for 'Tokyo' and 'Paris'. Please correct your 'location' argument to 'Tokyo' or 'Paris'."
        print(f"[OUTCOME] Tool failed. Unsupported location '{location}'.")
        return {
            "status": "error",
            "message": f"Destination '{location}' is not supported in the local database.",
            "supported_destinations": ["Tokyo", "Paris"],
            "guided_recovery": rec_msg
        }

    # Tokyo simulated attractions database
    if "tokyo" in loc_lower:
        results = [
            {
                "name": "Shinjuku Gyoen National Garden",
                "category": "Garden",
                "rating": 4.8,
                "description": "A spacious, beautiful park featuring Japanese traditional, English Landscape, and French Formal gardens. Ideal for relaxed strolls.",
                "hours": "9:00 AM - 4:30 PM",
                "vegan_friendly": True
            },
            {
                "name": "Meiji Jingu Shrine",
                "category": "Shrine / Historic",
                "rating": 4.7,
                "description": "A serene, forested Shinto shrine dedicated to Emperor Meiji and Empress Shoken. Features towering torii gates and peaceful walkways.",
                "hours": "Sunrise - Sunset",
                "vegan_friendly": True
            },
            {
                "name": "Takeshita Street",
                "category": "Shopping / Street Life",
                "rating": 4.3,
                "description": "The colorful, bustling epicenter of Tokyo's youth fashion and pop culture, packed with trendy boutiques, cafes, and creative dessert stands.",
                "hours": "10:00 AM - 8:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Tokyo Metropolitan Government Building",
                "category": "Landmark / Observatory",
                "rating": 4.6,
                "description": "Iconic twin towers in Shinjuku offering panoramic observation decks with views of Mount Fuji and the expansive city skyline.",
                "hours": "9:30 AM - 10:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Senso-ji Temple",
                "category": "Temple / Historic",
                "rating": 4.7,
                "description": "Tokyo's oldest and most iconic Buddhist temple in Asakusa, featuring a grand Kaminarimon gate and the bustling Nakamise shopping street.",
                "hours": "6:00 AM - 5:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Ueno Park",
                "category": "Park / Museum",
                "rating": 4.5,
                "description": "A spacious public park containing multiple world-class museums, a serene lotus pond, shrines, and beautiful cherry blossom walkways.",
                "hours": "5:00 AM - 11:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Kyushu Jangara Ramen (Harajuku)",
                "category": "Restaurant",
                "rating": 4.5,
                "description": "Famous for its hearty, authentic ramen. Offers a fully dedicated and highly rated vegan ramen menu.",
                "hours": "11:00 AM - 10:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Vegan Sushi Tokyo (Roppongi)",
                "category": "Restaurant",
                "rating": 4.9,
                "description": "Exquisite, artistic vegan sushi crafted from seasonal organic vegetables and traditional rice.",
                "hours": "12:00 PM - 9:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Vegan Restaurant Shibuya",
                "category": "Restaurant",
                "rating": 4.6,
                "description": "Modern plant-based bistro offering creative vegan burgers, organic salads, and craft drinks in Shibuya.",
                "hours": "11:30 AM - 10:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Vegan Ramen Shinjuku",
                "category": "Restaurant",
                "rating": 4.7,
                "description": "Incredibly rich, creamy plant-based tonkotsu and spicy sesame ramen bowls in the heart of Shinjuku.",
                "hours": "12:00 PM - 10:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Traditional Vegan Dining Asakusa",
                "category": "Restaurant",
                "rating": 4.8,
                "description": "Elegant Buddhist temple-style Shojin Ryori vegan multi-course dining near Senso-ji in Asakusa.",
                "hours": "11:30 AM - 9:30 PM",
                "vegan_friendly": True
            }
        ]
    # Paris simulated attractions database
    else:
        results = [
            {
                "name": "Jardin du Luxembourg",
                "category": "Garden",
                "rating": 4.8,
                "description": "Stunning public park with tree-lined promenades, fountains, flowerbeds, and classic statues. Perfect for a leisurely afternoon.",
                "hours": "7:30 AM - 9:30 PM",
                "vegan_friendly": True
            },
            {
                "name": "Musée de l'Orangerie",
                "category": "Museum",
                "rating": 4.7,
                "description": "An intimate art gallery of impressionist and post-impressionist paintings, housing Monet's famous Water Lilies.",
                "hours": "9:00 AM - 6:00 PM",
                "vegan_friendly": True
            },
            {
                "name": "Le Potager du Marais",
                "category": "Restaurant",
                "rating": 4.6,
                "description": "Cozy, traditional bistro serving organic French vegan dishes (like vegan beef bourguignon and crème brûlée).",
                "hours": "12:00 PM - 10:30 PM",
                "vegan_friendly": True
            }
        ]

    # Filter results by query matching
    filtered = [
        item for item in results
        if q_lower in item["name"].lower() or q_lower in item["category"].lower() or q_lower in item["description"].lower()
    ]

    # Return filtered, falling back to all results if filter returns empty
    final_list = filtered if filtered else results

    # Validate output schema
    try:
        validated_resp = SearchAttractionsResponse(location=inputs.location, attractions=final_list)
        out_dict = validated_resp.model_dump()
        print(f"[OUTCOME] Successfully found {len(final_list)} attractions in '{inputs.location}' matching query='{inputs.query}'")
        return out_dict
    except ValidationError as e:
        print(f"[OUTCOME] Error: Output serialization failed: {e.errors()}")
        return {"status": "error", "message": "Output schema validation failed."}


def check_weather(location: str, month: str) -> dict:
    """Retrieves typical monthly weather averages, forecasts, and packing recommendations.

    Args:
        location: The destination city. Supported: "Tokyo", "Paris".
        month: The name of the month (e.g. "August", "October").

    Returns:
        A dictionary with temperature averages, precipitation info, and packing tips.
    """
    # 📝 Intent Logging
    print(f"[INTENT] Tool 'check_weather' triggered with location='{location}' and month='{month}'")

    try:
        # Explicit Pydantic validation
        inputs = CheckWeatherInput(location=location, month=month)
    except ValidationError as e:
        err_msg = f"Argument validation failed for check_weather: {e.errors()}"
        print(f"[OUTCOME] Tool failed. {err_msg}")
        return {
            "status": "error",
            "message": "Argument validation failed.",
            "errors": e.errors(),
            "guided_recovery": "Please ensure you pass non-empty string arguments for 'location' and 'month'. Example: location='Tokyo', month='October'."
        }

    loc_lower = inputs.location.lower()
    month_lower = inputs.month.lower()

    # Guided recovery for unsupported locations
    if "tokyo" not in loc_lower and "paris" not in loc_lower:
        rec_msg = f"The database only contains seasonal weather reports for 'Tokyo' and 'Paris'. Please correct your 'location' argument to 'Tokyo' or 'Paris'."
        print(f"[OUTCOME] Tool failed. Unsupported location '{location}'.")
        return {
            "status": "error",
            "message": f"Weather data for '{location}' is not supported in the local database.",
            "supported_destinations": ["Tokyo", "Paris"],
            "guided_recovery": rec_msg
        }

    if "tokyo" in loc_lower:
        if month_lower in ["june", "july", "august", "september"]:
            avg_temp = "27°C (81°F)"
            conditions = "Hot and highly humid, with occasional rain showers."
            packing = "Lightweight breathable clothing, a compact umbrella, sunglasses, and comfortable walking sandals."
        else:
            avg_temp = "12°C (54°F)"
            conditions = "Cool, crisp, and sunny with clear blue skies."
            packing = "Layered clothing, a medium jacket, comfortable walking sneakers, and a scarf."
    else:
        if month_lower in ["june", "july", "august", "september"]:
            avg_temp = "22°C (72°F)"
            conditions = "Warm and pleasant with long sunny days."
            packing = "Light apparel, comfortable walking shoes, a sun hat, and a light jacket for cool evenings."
        else:
            avg_temp = "8°C (46°F)"
            conditions = "Chilly and overcast, with frequent light drizzle."
            packing = "Warm waterproof coat, layered sweaters, an umbrella, and solid waterproof boots."

    try:
        validated_resp = CheckWeatherResponse(
            location=inputs.location,
            month=inputs.month,
            average_temperature=avg_temp,
            conditions_summary=conditions,
            packing_recommendations=packing
        )
        out_dict = validated_resp.model_dump()
        print(f"[OUTCOME] Successfully retrieved weather for '{inputs.location}' in {inputs.month}")
        return out_dict
    except ValidationError as e:
        print(f"[OUTCOME] Error: Output serialization failed: {e.errors()}")
        return {"status": "error", "message": "Output schema validation failed."}


def format_itinerary(itinerary_data: dict) -> dict:
    """Takes a structured itinerary object and turns it into a high-fidelity Markdown layout.

    Args:
        itinerary_data: A dictionary containing the destination, duration, and day-by-day activities.

    Returns:
        A dictionary with the formatted markdown string.
    """
    # 📝 Intent Logging
    print(f"[INTENT] Tool 'format_itinerary' triggered to format itinerary.")

    try:
        # Explicit Pydantic validation
        inputs = ItineraryDataInput(**itinerary_data)
    except ValidationError as e:
        err_msg = f"Argument validation failed for format_itinerary: {e.errors()}"
        print(f"[OUTCOME] Tool failed. {err_msg}")
        return {
            "status": "error",
            "message": "Itinerary data validation failed. You must provide a valid structured itinerary matching the schema.",
            "errors": e.errors(),
            "guided_recovery": "Please correct the structure of your 'itinerary_data'. Ensure it has 'destination', 'duration', and a list of 'days', where each day has a 'day_title' and a list of 'activities' containing 'time', 'name', and 'description'."
        }

    destination = inputs.destination
    duration = inputs.duration
    days = inputs.days

    md_lines = []
    md_lines.append(f"# 🗺️ Custom Travel Itinerary: {destination} ({duration})")
    md_lines.append("Generated by **VoyageAI Travel Concierge**.\n")

    for i, day in enumerate(days, 1):
        day_title = day.day_title
        md_lines.append(f"## 📅 {day_title}")
        activities = day.activities
        if not activities:
            md_lines.append("*Relaxed free day to explore local sights on your own.*")
        for act in activities:
            time = act.time
            name = act.name
            description = act.description
            md_lines.append(f"* **{time}**: **{name}**")
            if description:
                md_lines.append(f"  * {description}")
        md_lines.append("")  # Empty line separator

    formatted_md = "\n".join(md_lines)
    print(f"[OUTCOME] Successfully compiled markdown itinerary for {destination} ({duration})")
    return {
        "status": "success",
        "markdown_itinerary": formatted_md
    }


def request_human_confirmation(action: str, reason: str) -> dict:
    """Requests explicit human confirmation for sensitive or high-impact actions (e.g. flight bookings, final itinerary locks).

    Args:
        action: The action that requires confirmation.
        reason: Why the action requires confirmation.

    Returns:
        A dictionary containing the confirmation pending status.
    """
    # 📝 Intent Logging
    print(f"[INTENT] Tool 'request_human_confirmation' triggered for action='{action}' (Reason: {reason})")

    try:
        inputs = ConfirmationRequest(action=action, reason=reason)
    except ValidationError as e:
        print(f"[OUTCOME] Tool failed. Validation error: {e.errors()}")
        return {
            "status": "error",
            "message": "Validation failed.",
            "errors": e.errors()
        }

    print(f"[OUTCOME] Human confirmation requested and pending for action='{inputs.action}'. Execution paused.")
    return {
        "status": "pending_confirmation",
        "action": inputs.action,
        "reason": inputs.reason,
        "message": f"CRITICAL: The action '{inputs.action}' is currently pending human confirmation. Reason: {inputs.reason}.",
        "guided_recovery": "You must wait for human feedback or present this confirmation block clearly in your final response so the user can approve it."
    }
