from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

app = FastAPI(title="VGI Numbering Engine", version="0.1.0")


class BBox(BaseModel):
    north: float = Field(..., description="Max latitude")
    south: float = Field(..., description="Min latitude")
    east: float = Field(..., description="Max longitude")
    west: float = Field(..., description="Min longitude")


class GenerateRequest(BaseModel):
    districtId: str = Field(..., description="Firestore district document id")
    bbox: BBox


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-zones-streets-bbox")
def generate_zones_streets(req: GenerateRequest):
    # Basic validation
    if req.bbox.north <= req.bbox.south:
        raise HTTPException(status_code=400, detail="Invalid bbox: north must be > south")
    if req.bbox.east <= req.bbox.west:
        raise HTTPException(status_code=400, detail="Invalid bbox: east must be > west")

    # Mock deterministic output (v1)
    # NOTE: Real GIS logic will replace this in later stages.
    zone_poly = {
        "type": "Polygon",
        "coordinates": [[
            [req.bbox.west, req.bbox.south],
            [req.bbox.east, req.bbox.south],
            [req.bbox.east, req.bbox.north],
            [req.bbox.west, req.bbox.north],
            [req.bbox.west, req.bbox.south],
        ]]
    }

    street_line = {
        "type": "LineString",
        "coordinates": [
            [req.bbox.west, (req.bbox.north + req.bbox.south) / 2],
