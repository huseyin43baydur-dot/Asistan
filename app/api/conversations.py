from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()

# Sample data for demonstration purposes
conversations = [
    {"id": 1, "date": "2026-03-29", "category": "work", "content": "Discussion about project timeline."},
    {"id": 2, "date": "2026-03-28", "category": "personal", "content": "Meeting with friends this weekend."},
    {"id": 3, "date": "2026-03-27", "category": "work", "content": "Feedback on the latest design."}
]

@app.get("/conversations", response_model=List[dict])
async def list_conversations(
    start_date: Optional[str] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Category to filter by"),
    search: Optional[str] = Query(None, description="Search keyword for conversation content")
)
    filtered_conversations = conversations

    # Filter by date range
    if start_date:
        filtered_conversations = [c for c in filtered_conversations if c['date'] >= start_date]
    if end_date:
        filtered_conversations = [c for c in filtered_conversations if c['date'] <= end_date]

    # Filter by category
    if category:
        filtered_conversations = [c for c in filtered_conversations if c['category'] == category]

    # Search functionality
    if search:
        filtered_conversations = [c for c in filtered_conversations if search.lower() in c['content'].lower()]

    return filtered_conversations
