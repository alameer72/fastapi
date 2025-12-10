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
    """
    نسخة تجريبية فقط:
    - تستقبل حدود الخريطة (BBox)
    - ترجع FeatureCollection فيها بلوكين وهميين
    الهدف: اختبار الربط مع n8n و Vercel قبل إدخال GIS حقيقي.
    """

    # نحسب نقطة منتصف الـ BBox بشكل بسيط
    mid_lat = (bbox.north + bbox.south) / 2
    mid_lon = (bbox.east + bbox.west) / 2

    # نصنع بلوكين صغيرين حول المنتصف (مربعات وهمية)
    block1 = {
        "type": "Feature",
        "properties": {"block_id": 1},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [mid_lon - 0.001, mid_lat - 0.001],
                [mid_lon - 0.001, mid_lat + 0.001],
                [mid_lon + 0.001, mid_lat + 0.001],
                [mid_lon + 0.001, mid_lat - 0.001],
                [mid_lon - 0.001, mid_lat - 0.001],
            ]]
        },
    }

    block2 = {
        "type": "Feature",
        "properties": {"block_id": 2},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [mid_lon + 0.002, mid_lat - 0.001],
                [mid_lon + 0.002, mid_lat + 0.001],
                [mid_lon + 0.004, mid_lat + 0.001],
                [mid_lon + 0.004, mid_lat - 0.001],
                [mid_lon + 0.002, mid_lat - 0.001],
            ]]
        },
    }

    feature_collection = {
        "type": "FeatureCollection",
        "features": [block1, block2],
    }

    return feature_collection
