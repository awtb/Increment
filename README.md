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
<h3>📈 Performance Benchmark: <code>/api/v1/increment</code> vs <code>/api/v2/increment</code></h3>

<h4>Summary</h4>
<table border="1" cellpadding="6" cellspacing="0">
  <thead>
    <tr>
      <th>Metric</th>
      <th>/api/v1/increment</th>
      <th>/api/v2/increment</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>Total Requests</strong></td><td>65,230</td><td>434,079</td></tr>
    <tr><td><strong>Failures</strong></td><td>0 (0.00%)</td><td>0 (0.00%)</td></tr>
    <tr><td><strong>Average Response Time (ms)</strong></td><td>349</td><td>62</td></tr>
    <tr><td><strong>Median Response Time (ms)</strong></td><td>380</td><td>13</td></tr>
    <tr><td><strong>Max Response Time (ms)</strong></td><td>2363</td><td>7368</td></tr>
    <tr><td><strong>Requests/sec (throughput)</strong></td><td>~2359</td><td>~5125</td></tr>
  </tbody>
</table>

<h4>Response Time Percentiles</h4>
<table border="1" cellpadding="6" cellspacing="0">
  <thead>
    <tr>
      <th>Percentile</th>
      <th>/api/v1/increment (ms)</th>
      <th>/api/v2/increment (ms)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>50%</td><td>380</td><td>13</td></tr>
    <tr><td>75%</td><td>400</td><td>85</td></tr>
    <tr><td>90%</td><td>520</td><td>190</td></tr>
    <tr><td>95%</td><td>760</td><td>230</td></tr>
    <tr><td>98%</td><td>870</td><td>250</td></tr>
    <tr><td>99%</td><td>910</td><td>270</td></tr>
    <tr><td>99.9%</td><td>1300</td><td>2900</td></tr>
    <tr><td>99.99%</td><td>2000</td><td>6100</td></tr>
    <tr><td>100%</td><td>2400</td><td>7368</td></tr>
  </tbody>
</table>

<h4>Insights</h4>
<ul>
  <li><code>/api/v2/increment</code> is <strong>~5–6x faster</strong> on average.</li>
  <li>Handles <strong>~7x more requests</strong> during the same duration.</li>
  <li>Significant latency improvements across all percentiles.</li>
  <li>No request failures in either version.</li>
  <li>CPU usage reached high levels — consider <a href="https://docs.locust.io/en/stable/running-distributed.html" target="_blank">distributed load testing</a> if scaling further.</li>
</ul>
