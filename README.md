# Increment - a high performance counter API
This project focuses on developing a highly optimized API endpoint for incrementing an integer field stored in a single-row database table. The primary goal is to maximize requests per second (RPS) by exploring various performance optimizations.

## Tech Stack

- **Language:** Python  
- **Web Framework:** BlackSheep  
- **Database:** PostgreSQL  

## Overview

- The database contains a single row with one `INTEGER` column.  
- The API provides an endpoint to atomically increment this field.  
- The main objective is to push the RPS to its limits.  

## Endpoints list
## API Endpoints

| Method | Endpoint            | Description                                      | Version |
|--------|---------------------|--------------------------------------------------|---------|
| POST   | `/api/v1/increment`  | Increment a single integer field (v1 - baseline) | v1      |
| POST   | `/api/v2/increment`  | Optimized increment endpoint with higher performance | v2  |

More details on implementation and benchmarking will be added as the project evolves.

## Installation
```bash
git clone https://github.com/awtb/Increment
```

### Configuring project
Create `.env` file
```
touch .env
```

You can fill it using this template.
```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=increment
DB_PASSWORD=ilyas
DB_USER=ilyas
SERVING_PORT=8000
```


### Running project
#### First option, using `docker compose`
```
docker compose up
```

#### Second option, by hand

Make sure you have [UV](https://docs.astral.sh/uv/) installed

**Create virtual env**
```bash
uv venv 
```
**Install dependencies**
```bash
uv sync --frozen
```

**Run project**
```bash
uv run scripts/prod.sh
```

## Benchmarking 

We use [Locust](https://locust.io/) for load testing.  

You can run it using cmd below

#### Benchmarking slow version
```bash
uv run locust -f src/tests/load/increment.py
```

#### Benchmarking fast version
```bash
uv run locust -f src/tests/load/increment_v2.py
```

## My results
### 📈 Performance Benchmark: `/api/v1/increment` vs `/api/v2/increment`

#### Summary

| Metric                         | `/api/v1/increment` | `/api/v2/increment` |
|-------------------------------|---------------------|---------------------|
| **Total Requests**            | 65,230              | 434,079             |
| **Failures**                  | 0 (0.00%)           | 0 (0.00%)           |
| **Average Response Time (ms)**| 349                 | 62                  |
| **Median Response Time (ms)** | 380                 | 13                  |
| **Max Response Time (ms)**    | 2363                | 7368                |
| **Requests/sec (throughput)** | ~2359               | ~5125               |

#### Response Time Percentiles

| Percentile | `/api/v1/increment (ms)` | `/api/v2/increment (ms)` |
|------------|---------------------------|---------------------------|
| 50%        | 380                       | 13                        |
| 75%        | 400                       | 85                        |
| 90%        | 520                       | 190                       |
| 95%        | 760                       | 230                       |
| 98%        | 870                       | 250                       |
| 99%        | 910                       | 270                       |
| 99.9%      | 1300                      | 2900                      |
| 99.99%     | 2000                      | 6100                      |
| 100%       | 2400                      | 7368                      |

#### Insights

- `/api/v2/increment` is **~5–6x faster** on average.
- Handles **~7x more requests** during the same duration.
- Significant latency improvements across all percentiles.
- No request failures in either version.
- CPU usage reached high levels — consider [distributed load testing](https://docs.locust.io/en/stable/running-distributed.html) if scaling further.
