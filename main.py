from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BBox(BaseModel):
    north: float
    south: float
    east: float
    west: float


@app.get("/")
def health_check():
    return {"status": "ok", "service": "VGI Numbering Engine (stub)"}


@app.post("/generate-blocks-bbox")
def generate_blocks(bbox: BBox):
    # simple dummy response just for testing
    mid_lat = (bbox.north + bbox.south) / 2
    mid_lon = (bbox.east + bbox.west) / 2

    block = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"block_id": 1},
                "geometry": {
                    "type": "Point",
                    "coordinates": [mid_lon, mid_lat],
                },
            }
        ],
    }

    return block
