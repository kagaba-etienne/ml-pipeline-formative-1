from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    Open: float = Field(..., description="Opening price")
    High: float = Field(..., description="Highest price")
    Low: float = Field(..., description="Lowest price")
    Volume: float = Field(..., description="Trading volume")
    Lag1: float = Field(..., description="Lag1 feature")
    MA7: float = Field(..., description="7-day moving average")
    Return: float = Field(..., description="Return feature")
    Year: int = Field(..., description="Year")
    Month: int = Field(..., description="Month")
    Day: int = Field(..., description="Day")
    DayOfWeek: int = Field(..., description="Day of the week")
    Name_CAT: int = Field(0, description="1 if name is CAT else 0")
    Name_JPM: int = Field(0, description="1 if name is JPM else 0")
    Name_MCD: int = Field(0, description="1 if name is MCD else 0")
    Name_WMT: int = Field(0, description="1 if name is WMT else 0")

class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="The predicted value")
