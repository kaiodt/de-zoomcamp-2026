# Homework 02

## Setup

- Make sure to follow the [setup instructions](../kestra) to set up the Kestra server and the GCP credentials.

- Upload the following flows to the Kestra UI:

    - [01_gcp_kv_setup.yaml](01_gcp_kv_setup.yaml)
    - [02_gcp_services_setup.yaml](02_gcp_services_setup.yaml)
    - [03_gcp_taxi_ingestion_scheduled.yaml](03_gcp_taxi_ingestion_scheduled.yaml)

- Run the first two flows manually to set up the Key-Value pairs and GCP resources.

- Run a backfill for the third flow from `2020-01-01` to `2020-12-31` for the `Yellow` and `Green` taxis.

- Run a backfill for the third flow from `2021-03-01` to `2021-03-02` for the `Yellow` taxi.


## Question 01

Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: What is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

### Solution

To figure out the uncompressed file size, we need to look at the output of the `extract` task for the execution for `Yellow` Taxi data for the year `2020` and month `12`.

1. Find the execution for `Yellow` Taxi data for the year `2020` and month `12`.
2. Look at the output of the `extract` task.
3. The output is `yellow_tripdata_2020-12.csv`.

**The result is: `128.3 MiB`**


## Question 02

What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

### Solution

**The rendered value is: `green_tripdata_2020-04.csv`**


## Question 03

How many rows are there for the `Yellow` Taxi data for all CSV files in the year `2020`?

### Solution

Since we ran a backfill for the Yellow Taxi data for the year `2020`, we can query the `yellow_tripdata` table to count all rows where the source filename contains `2020`:

```sql
SELECT COUNT(1)
FROM `de-zoomcamp.taxi_tripdata.yellow_tripdata`
WHERE filename LIKE '%2020%'
```

**The result is: `24,648,499`**


## Question 04

How many rows are there for the `Green` Taxi data for all CSV files in the year `2020`?

### Solution

Since we ran a backfill for the Green Taxi data for the year `2020`, we can query the `green_tripdata` table to count all rows where the source filename contains `2020`:

```sql
SELECT COUNT(1)
FROM `de-zoomcamp.taxi_tripdata.green_tripdata`
WHERE filename LIKE '%2020%'
```

**The result is: `1,734,051`**


## Question 05

How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

### Solution

Since we ran a backfill for the Yellow Taxi data for March 2021, we can query the `yellow_tripdata` table to count all 
rows where the source filename contains `2021-03`:

```sql
SELECT COUNT(1)
FROM `de-zoomcamp.taxi_tripdata.yellow_tripdata`
WHERE filename LIKE '%2021-03%'
```

**The result is: `1,925,152`**


## Question 06

How would you configure the timezone to New York in a Schedule trigger?


## Solution

We add the property:

```yaml
schedule:
  timezone: America/New_york
```

**The result is: `America/New_York`**
