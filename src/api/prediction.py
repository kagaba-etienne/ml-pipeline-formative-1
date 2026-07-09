from fastapi import APIRouter, Depends, HTTPException
from src.schemas.prediction import PredictionRequest, PredictionResponse
from src.services.prediction_service import PredictionService, get_prediction_service

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

@router.post("/", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    try:
        prediction = service.predict(request.model_dump())
        return PredictionResponse(prediction=prediction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
