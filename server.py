from fastmcp import FastMCP
import json
import os

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

if __name__ == "__main__":
    mcp.run()