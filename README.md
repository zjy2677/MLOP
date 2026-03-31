# MLOP – House Price Calculator (FRANCE) - Streamlit Cloud Version

This repository contains a simple **HOUSE PRICE CALCULATOR** for estimating house prices in FRANCE, it also has the ability to identify that ,given a surface area(m^2) and its price(euros), the pricing is reasonable.

The project is designed as a learning-oriented backend service to 
- Region: Whole France 
- Goal: Given a house in any city in France, we want an instant but primary inspection of it and have a general understanding of its price

------------------------------------------
# Data Source

We use data from DVF of the past years and group by with cities. 
Thus, we were able to calculate a average price estimator of house in euros/ m^2


```text
Project structure:

├── backend/
│   ├── services/
│   │   ├── anomaly.py
│   │   ├── scoring.py
│   └── requirements.txt
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   ├── city_price_benchmark.csv (This is the complete data file)
│   └── sample.csv (This contains nothing for now)
│
├── .env.example
├── .gitignore
└── README.md
```
We seperated our repo into the following parts:<br>
(1)**backend**: This will contains a service folder which has scoring.py that calculates the overall score of the house and a anomaly.py that examine if alarm should be triggered. Main.py is for an entry-point to our backend logic. Requirement.txt contains settings and requirements for running all the backend files.<br>

(2)**frontend**: This folder contains an app.py which defines our UI. Requirements.txt in this folder will ensure all necessary elements used in app.py are installed.<br>

(3)**Data**: Data folder contains a city_price_benchmark which contains average price of house in a specific city. Sample.csv contains a small part of the database for testing purpose only.<br>

(4)**.env.example**: Template of environment in case we need to hide some secrets like API keys.<br>

(5)**.gitignore**: Prevents potential leakage of sensitive data and avoids unnecessary files

------------------------------------------
## Methodology (Backend)

Our backend follows a simple rule-based pipeline powered by the benchmark table in `data/city_price_benchmark.csv`.

### 1) Load city benchmark data
- At startup, the API loads benchmark data from `city_price_benchmark.csv`.
- Each row contains a city (`Commune`) and its average price per square meter (`avg_price_m2`).

### 2) House price estimation logic
For each `price` request (`city`, `surface`):
1. Validate `surface` is numeric and strictly greater than 0.
2. Look up the city in the benchmark table.
3. Compute a baseline estimate:

`estimated_price = surface * avg_price_m2(city)`

This gives a reference value for the input property.

### 3) Anomaly detection logic
For each `anomaly` request (`city`, `surface`, `actual_price`):
1. Recompute the same baseline `estimated_price` using the scoring method above.
2. Build a tolerance interval around the estimate:
   - `lower_bound = 0.8 × estimated_price`
   - `upper_bound = 1.3 × estimated_price`
3. Classify pricing status with simple rules:
   - `actual_price < lower_bound`  → `anomaly_underprice`
   - `actual_price > upper_bound`  → `anomaly_overprice`
   - otherwise                     → `normal`

------------------------------------------
## How to Run (Streamlit UI)
This version has the same backend logic as the docker version.  
You can simply run this app by visiting this website:  
[House Price Calculator App](https://mlophousepricecalculator-fnakg32aiswfdrvcwtbzoh.streamlit.app/)







