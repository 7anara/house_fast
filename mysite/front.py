import streamlit as st
import requests


api_url = 'http://127.0.0.1:8000/predict/'


nei_list = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr',
            'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV',
            'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge',
            'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW',
            'Somerst', 'StoneBr', 'Timber', 'Veenker']

st.title('House price forecast')

area = st.number_input('House area:', value=0)
year = st.number_input('Year:', value=0)
garage = st.number_input('Garage capacity:', value=0)
bsmt = st.number_input('Basement area:', value=0)
bath = st.number_input('Bathroom quantity:', value=0)
overall_qual = st.number_input('Overall quality:', value=0)
neighborhood = st.selectbox('Neighborhood:', nei_list)

data = {
    "GrLivArea": area,
    "YearBuilt": year,
    "GarageCars": garage,
    "TotalBsmtSF": bsmt,
    "FullBath": bath,
    "OverallQual": overall_qual,
    "Neighborhood": neighborhood
}


if st.button('Predict'):
    try:
        answer = requests.post(api_url, json=data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f'Result: {result.get('Price')}')

        else:
            st.error(f'Error : {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error(f'Failed to connect to API')