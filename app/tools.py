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

"""Specialized travel planning tools for VoyageAI."""

def search_attractions(location: str, query: str) -> dict:
    """Searches for localized attractions, landmarks, restaurants, and reviews.

    Args:
        location: The city or area to search in (e.g. "Tokyo", "Paris").
        query: Specific keyword to filter attractions (e.g. "gardens", "vegan sushi").

    Returns:
        A dictionary containing a list of matching attractions with ratings and descriptions.
    """
    location_lower = location.lower()
    query_lower = query.lower()

    # Tokyo simulated attractions database
    if "tokyo" in location_lower:
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
            }
        ]
    # Paris simulated attractions database
    elif "paris" in location_lower:
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
    else:
        results = [
            {
                "name": f"Local Discovery in {location}",
                "category": "General Landmark",
                "rating": 4.4,
                "description": f"A historic and picturesque spot in the heart of {location} that captures the local culture.",
                "hours": "Open 24 Hours",
                "vegan_friendly": True
            }
        ]

    # Filter results by query matching
    filtered = [
        item for item in results
        if query_lower in item["name"].lower() or query_lower in item["category"].lower() or query_lower in item["description"].lower()
    ]

    # Return filtered, falling back to all results if filter returns empty
    final_list = filtered if filtered else results
    return {"status": "success", "location": location, "attractions": final_list}


def check_weather(location: str, month: str) -> dict:
    """Retrieves typical monthly weather averages, forecasts, and packing recommendations.

    Args:
        location: The destination city (e.g. "Tokyo", "Paris").
        month: The name of the month (e.g. "August", "December").

    Returns:
        A dictionary with temperature averages, precipitation info, and packing tips.
    """
    location_lower = location.lower()
    month_lower = month.lower()

    if "tokyo" in location_lower:
        if month_lower in ["june", "july", "august", "september"]:
            avg_temp = "27°C (81°F)"
            conditions = "Hot and highly humid, with occasional rain showers."
            packing = "Lightweight breathable clothing, a compact umbrella, sunglasses, and comfortable walking sandals."
        else:
            avg_temp = "12°C (54°F)"
            conditions = "Cool, crisp, and sunny with clear blue skies."
            packing = "Layered clothing, a medium jacket, comfortable walking sneakers, and a scarf."
    elif "paris" in location_lower:
        if month_lower in ["june", "july", "august", "september"]:
            avg_temp = "22°C (72°F)"
            conditions = "Warm and pleasant with long sunny days."
            packing = "Light apparel, comfortable walking shoes, a sun hat, and a light jacket for cool evenings."
        else:
            avg_temp = "8°C (46°F)"
            conditions = "Chilly and overcast, with frequent light drizzle."
            packing = "Warm waterproof coat, layered sweaters, an umbrella, and solid waterproof boots."
    else:
        avg_temp = "18°C (64°F)"
        conditions = "Moderate, mild climate."
        packing = "Comfortable layered wear, walking shoes, and a light jacket."

    return {
        "status": "success",
        "location": location,
        "month": month,
        "average_temperature": avg_temp,
        "conditions_summary": conditions,
        "packing_recommendations": packing
    }


def format_itinerary(itinerary_data: dict) -> dict:
    """Takes a structured itinerary object and turns it into a high-fidelity Markdown layout.

    Args:
        itinerary_data: A dictionary containing the destination, duration, and day-by-day activities.

    Returns:
        A dictionary with the formatted markdown string.
    """
    destination = itinerary_data.get("destination", "Your Destination")
    duration = itinerary_data.get("duration", "Custom Duration")
    days = itinerary_data.get("days", [])

    md_lines = []
    md_lines.append(f"# 🗺️ Custom Travel Itinerary: {destination} ({duration})")
    md_lines.append("Generated by **VoyageAI Travel Concierge**.\n")

    for i, day in enumerate(days, 1):
        day_title = day.get("day_title", f"Day {i}")
        md_lines.append(f"## 📅 {day_title}")
        activities = day.get("activities", [])
        if not activities:
            md_lines.append("*Relaxed free day to explore local sights on your own.*")
        for act in activities:
            time = act.get("time", "flexible")
            name = act.get("name", "Activity")
            description = act.get("description", "")
            md_lines.append(f"* **{time}**: **{name}**")
            if description:
                md_lines.append(f"  * {description}")
        md_lines.append("")  # Empty line separator

    formatted_md = "\n".join(md_lines)
    return {
        "status": "success",
        "markdown_itinerary": formatted_md
    }
