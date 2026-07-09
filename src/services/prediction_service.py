import pickle
import joblib
import pandas as pd
from typing import Dict, Any

class PredictionService:
    def __init__(self, model_path: str, feature_order_path: str):
        with open(model_path, 'rb') as f:
            self.model = joblib.load(f)
        with open(feature_order_path, 'rb') as f:
            self.feature_order = pickle.load(f)
            
    def predict(self, input_data: Dict[str, Any]) -> float:
        # Create DataFrame from input to ensure ordering and shape
        df = pd.DataFrame([input_data])
        # Ensure features are in the exact order expected by the model
        X = df[self.feature_order]
        prediction = self.model.predict(X)[0]
        return float(prediction)

prediction_service = None

def get_prediction_service() -> PredictionService:
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService(
            model_path='model/linear_regression_model.pkl',
            feature_order_path='model/feature_order.pkl'
        )
    return prediction_service
