from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.scoring import score_house_price


app = FastAPI(title="House Price Calculator API", version="0.1.0")


class HousePriceRequest(BaseModel):
    area_m2: float = Field(..., gt=0, le=2000, description="Total area in square meters")
    bedrooms: int = Field(..., ge=0, le=20)
    bathrooms: int = Field(..., ge=0, le=20)
    location_score: float = Field(..., ge=0, le=10, description="0 (weak) to 10 (premium)")
    year_built: int = Field(..., ge=1800, le=2100)
    has_garage: bool = False
    has_garden: bool = False
    energy_rating: str = Field(..., description="Energy rating: A, B, C, D, E, F, or G")


class HousePriceResponse(BaseModel):
    estimated_price: float
    currency: str = "EUR"
    confidence: float
    breakdown: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/house-price", response_model=HousePriceResponse)
def calculate_house_price(payload: HousePriceRequest):
    try:
        result = score_house_price(
            area_m2=payload.area_m2,
            bedrooms=payload.bedrooms,
            bathrooms=payload.bathrooms,
            location_score=payload.location_score,
            year_built=payload.year_built,
            has_garage=payload.has_garage,
            has_garden=payload.has_garden,
            energy_rating=payload.energy_rating,
        )
    except ValueError as e:
        # scoring.py raises ValueError for invalid energy_rating, etc.
        raise HTTPException(status_code=422, detail=str(e))

    return HousePriceResponse(
        estimated_price=result.estimated_price,
        confidence=result.confidence,
        breakdown={
            "base": result.base,
            "area_component": result.area_component,
            "rooms_component": result.rooms_component,
            "location_component": result.location_component,
            "features_component": result.features_component,
            "age_component": result.age_component,
            "energy_component": result.energy_component,
        },
    )
