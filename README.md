# Increment - a high performance counter API
This project focuses on developing a highly optimized API endpoint for incrementing an integer field stored in a single-row database table. The primary goal is to maximize requests per second (RPS) by exploring various performance optimizations.

## Tech Stack

- **Language:** Python  
- **Web Framework:** BlackSheep  
- **Database:** PostgreSQL / MySQL / SQLite  

## Overview

- The database contains a single row with one `INTEGER` column.  
- The API provides an endpoint to atomically increment this field.  
- The main objective is to push the RPS to its limits.  

More details on implementation and benchmarking will be added as the project evolves.

## Installation
Wil be added soon...

## Benchmarking 

We use [Locust](https://locust.io/) for load testing.  

You can run it using cmd below

```bash
uv run locust -f src/tests/load/increment.py
```