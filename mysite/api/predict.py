from fastapi import APIRouter
from mysite.database.schema import HousePredictSchema
import joblib


model = joblib.load('mysite/ml_models/model.pkl')
scaler = joblib.load('mysite/ml_models/scaler.pkl')


new_list = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr',
            'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV',
            'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge', 'NridgHT',
            'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr',
            'Timber', 'Veenker']


predict_router = APIRouter(prefix='/predict', tags=['Predict Price'])



@predict_router.post('/')
async def predict_price(house: HousePredictSchema):
    house_dict = house.dict()

    name_nei = house_dict.pop('Neighborhood')
    name_nei1_0 = [
        1 if name_nei == i else 0 for i in new_list
    ]

    house_data = list(house_dict.values()) + name_nei1_0
    scaler_data = scaler.transform([house_data])
    pred = model.predict(scaler_data)[0]

    return {'Price': round(pred)}


