# Increment - High Performance Counter API

This project is focused on building a highly optimized API endpoint for incrementing an integer field stored in a single-row database table. The primary goal is to maximize requests per second (RPS) by exploring various performance optimizations.

## Tech Stack

* **Language:** Python
* **Web Framework:** BlackSheep
* **Database:** PostgreSQL

## Overview

* The database contains a single row with one `INTEGER` column.
* The API provides endpoints to atomically increment this field and retrieve the current count.
* The objective is to push the RPS to its limits through iterative optimization.

## API Endpoints

| Method | Endpoint          | Description                            | Version |
| ------ | ----------------- | -------------------------------------- | ------- |
| POST   | `/api/v1/counter` | Increment the integer field            | v1      |
| GET    | `/api/v1/counter` | Get current value of the integer field | v1      |

## Installation

Clone the repository:

```bash
git clone https://github.com/awtb/Increment
```

### Configuration

Create an `.env` file:

```bash
touch .env
```

Template:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=increment
DB_PASSWORD=ilyas
DB_USER=ilyas
SERVING_PORT=8000
```

### Running the Project

#### Option 1: Docker Compose

**Using prebuilt image:**

```bash
docker compose up
```

**Building manually:**

```bash
docker compose up --build
```

#### Option 2: Kubernetes

Apply manifests:

```bash
kubectl apply -f ./k8s
```

#### Option 3: Manual Setup

Make sure you have [UV](https://docs.astral.sh/uv/) installed.

**Create virtual environment:**

```bash
uv venv
```

**Install dependencies:**

```bash
uv sync --frozen
```

**Run project:**

```bash
uv run scripts/prod.sh
```

## Benchmarking

We use [Locust](https://locust.io/) for load testing.

#### Run benchmark:

```bash
uv run locust -f src/tests/load/counter.py
```

## Performance Results

### `/api/v1/counter` (increment endpoint)

| Metric                         | Value     |
| ------------------------------ | --------- |
| **Total Requests**             | 281,000   |
| **Failures**                   | 0 (0.00%) |
| **Average Response Time (ms)** | \~215     |
| **Median Response Time (ms)**  | 190       |
| **Max Response Time (ms)**     | 1250      |
| **Throughput (req/sec)**       | \~4630    |


### Key Insights

* Stable throughput around **\~4600 RPS** with no request failures.
* Latency remains consistent across higher percentiles.
* CPU is the main bottleneck.
* Due to the design, we cannot truly scale horizontally since it forces the use of a single core.

## Development Environment

A `.devcontainer/devcontainer.json` is provided for VS Code or PyCharm integration to ensure consistent development environments.
