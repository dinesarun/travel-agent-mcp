from fastmcp import FastMCP
import json
import os
import requests

# 1. Initialize the Server
mcp = FastMCP("Expedia-Prototype")
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookings.json")

# Helper to ensure DB exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

@mcp.tool()
def create_booking(hotel_name: str, city: str, nights: int) -> str:
    """Registers a new hotel booking. Use this when a user wants to book a stay."""
    with open(DB_FILE, "r+") as f:
        bookings = json.load(f)
        new_entry = {"hotel": hotel_name, "city": city, "nights": nights}
        bookings.append(new_entry)
        f.seek(0)
        json.dump(bookings, f, indent=2)
    return f"Success! Booked {hotel_name} in {city} for {nights} nights."

@mcp.tool()
def list_bookings() -> str:
    """Retrieves all current travel bookings."""
    with open(DB_FILE, "r") as f:
        bookings = json.load(f)
    return json.dumps(bookings)

# The Backstage Backend API URL
BACKSTAGE_API = "http://127.0.0.1:7007/api/catalog"

@mcp.tool()
def get_backstage_catalog() -> str:
    """Fetches all components currently registered in the Backstage Catalog."""
    try:
        # We query the entities endpoint
        response = requests.get(f"{BACKSTAGE_API}/entities", params={"filter": "kind=component"})
        response.raise_for_status()
        entities = response.json()
        
        if not entities:
            return "The catalog is currently empty."
            
        # Format the names for the AI to understand
        component_names = [e['metadata']['name'] for e in entities]
        return f"I found the following components in the catalog: {', '.join(component_names)}"
        
    except Exception as e:
        return f"Failed to connect to Backstage: {str(e)}. Make sure 'yarn start' is running!"
    

import os
import yaml

# Path to your Backstage 'examples' folder so it shows up in the UI
BACKSTAGE_EXAMPLES_PATH = "/Users/dinesh/expedia-portal/examples" 

@mcp.tool()
def register_new_service(name: str, description: str) -> str:
    """Creates a new YAML definition for a service in the local Backstage catalog."""
    file_name = f"{name.lower().replace(' ', '-')}.yaml"
    file_path = os.path.join(BACKSTAGE_EXAMPLES_PATH, file_name)
    
    # Standard Backstage Component Metadata
    data = {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": name.lower().replace(' ', '-'),
            "description": description,
            "annotations": {
                "github.com/project-slug": f"dinesarun/{name.lower().replace(' ', '-')}"
            }
        },
        "spec": {
            "type": "service",
            "lifecycle": "experimental",
            "owner": "guests"
        }
    }

    try:
        with open(file_path, "w") as f:
            yaml.dump(data, f)
        return f"Successfully created {file_name} in Backstage. Refresh your browser to see it!"
    except Exception as e:
        return f"Failed to write file: {str(e)}"
    
if __name__ == "__main__":
    mcp.run()