# Homework 05

## Setup

- Install Bruin CLI:

    ```bash
    curl -LsSf https://getbruin.com/install/cli | sh
    ```

- Initialize the zoomcamp template:

    ```bash
    bruin init zoomcamp my-pipeline
    ```

- Configure your `.bruin.yml` with a DuckDB connection.

- Follow the tutorial in the main module README.

- After completing the setup, you should have a working NYC taxi data pipeline.

---

## Question 01 - Bruin Pipeline Structure

In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

### Solution

**The correct answer is: `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`**

---

## Question 02 - Materialization Strategies

You're building a pipeline that processes NYC taxi data organized by month based on `pickup_datetime`. Which materialization strategy should you use for the staging layer that deduplicates and cleans the data?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column
- `view` - create a virtual table only

### Solution

**The correct answer is: `time_interval` - incremental based on a time column**

---

## Question 03 - Pipeline Variables

You have the following variable defined in `pipeline.yml`:

```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

How do you override this when running the pipeline to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'`
- `bruin run --set taxi_types=["yellow"]`

### Solution

**The correct answer is: `bruin run --var 'taxi_types=["yellow"]'`**

---

## Question 04 - Running with Dependencies

You've modified the `ingestion/trips.py` asset and want to run it plus all downstream assets. Which command should you use?

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream`
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

### Solution

**The correct answer is: `bruin run ingestion/trips.py --downstream`**

---

## Question 05 - Quality Checks

You want to ensure the `pickup_datetime` column in your trips table never has `NULL` values. Which quality check should you add to your asset definition?

- `unique: true`
- `not_null: true`
- `positive: true`
- `accepted_values: [not_null]`

### Solution

**The correct answer is: `not_null: true`**

---


## Question 06 - Lineage and Dependencies

After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

### Solution

**The correct answer is: `bruin lineage`**

---

## Question 07 - First-Time Run

You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

### Solution

**The correct answer is: `--full-refresh`**
