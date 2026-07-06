from fastapi import FastAPI, Query, HTTPException
from typing import List
from .reader import load_all_proverbs, load_proverbs_by_fidel, get_random_proverb, search_proverbs

app = FastAPI(
    title="Temsalet API",
    description="An API to retrieve and search traditional Ethiopian proverbs with pagination support.",
    version="1.0.0"
)

@app.get("/proverbs", summary="Retrieve all proverbs (Paginated)")
async def read_all(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max number of records to return")
):
    return load_all_proverbs(skip=skip, limit=limit)

@app.get("/proverbs/fidel/{letter}", summary="Retrieve proverbs by starting letter (Paginated)")
async def read_by_fidel(
    letter: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max number of records to return")
):
    """
    Get proverbs starting with a specific Amharic character (Fidel).
    """
    results = load_proverbs_by_fidel(letter, skip=skip, limit=limit)
    if not results and skip == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No proverbs starting with '{letter}' were found."
        )
    return results

@app.get("/proverbs/random", summary="Get a random proverb")
async def read_random():
    proverb = get_random_proverb()
    if not proverb:
        raise HTTPException(status_code=404, detail="No proverbs found")
    return proverb

@app.get("/proverbs/search", summary="Search across all proverbs")
async def search(
    q: str = Query(..., description="Search term in Amharic or English"),
    limit: int = Query(20, ge=1, le=50, description="Max search results")
):
    return search_proverbs(q, limit=limit)

def run():
    import uvicorn
    uvicorn.run("temsalet.main:app", host="127.0.0.1", port=8000, reload=True)
