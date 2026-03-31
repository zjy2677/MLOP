# MLOP – House Price Calculator (FRANCE)

This repository contains a simple **HOUSE PRICE CALCULATOR** for estimating house prices in FRANCE, it also has the ability to identify if , given a surface area(square meter) and its price(euros), the pricing is reasonable.

------------------------------------------
# Data Source

We use data from DVF of the past years and group by with cities. 
Thus, we were able to calculate a average price estimator of house in euros per squared meter.


```text
Project structure:

├── backend/
│   ├── services/
│   │   ├── anomaly.py
│   │   ├── scoring.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/
│   ├── city_price_benchmark.csv (This is the complete data file)
│   └── sample.csv (This contains test data sample)
│
├── .env.example
├── .gitignore
└── README.md
```
We seperated our repo into the following parts:<br>
(1)**backend**: This will contain a service folder which has scoring.py that calculates the price of the house and a anomaly.py that examine if alarm should be triggered. Main.py is for an entry-point to our backend logic where we run fastAPI service. Dockerfile and requirement.txt contains settings and requirements for running all the backend files.<br>

(2)**frontend**: This folder contains an app.py which defines our UI. Dockerfile and requirements.txt in this folder will ensure all necessary elements used in app.py are installed.<br>

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
## How to Run (Docker - Codespaces)

Follow these steps to build and run the application using Docker.

---

### 1. Build Docker Images

Build both backend and frontend images:

```bash
docker build -f backend/Dockerfile -t house-backend .
docker build -f frontend/Dockerfile -t house-frontend .
```

---

### 2. Create a Docker Network

Create a shared network so containers can communicate:

```bash
docker network create house-net
```

---

### 3. Run the Backend Container

Start the backend service:

```bash
docker run -d \
  --name house-backend-container \
  --network house-net \
  -p 8000:8000 \
  house-backend
```

---

### 4. Run the Frontend Container

Start the frontend service:

```bash
docker run -d \
  --name house-frontend-container \
  --network house-net \
  -p 8501:8501 \
  -e BACKEND_URL="http://house-backend-container:8000" \
  house-frontend
```

---

## Access the Application

- Frontend: http://localhost:8501  
- Backend API: http://localhost:8000

------------------------------------------
## Where to improve

(1) We used a rather naive prediction model: predicted_price = average price * surface area.<br>
(2) We can enrich features (district, property age, rooms, floor, energy rating) and train a regression model to reduce bias from city-level average <br>
(2) We could use a google gemini api to build a chatbot that further assists our customer in using this app <br>


