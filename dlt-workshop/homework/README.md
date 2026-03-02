# Homework - dlt Workshop

## The Challenge

For this homework, build a dlt pipeline that loads NYC taxi trip data from a custom API into DuckDB and then answer some questions using the loaded data.

## Data Source

You'll be working with NYC Yellow Taxi trip data from a custom API (not available as a dlt scaffold). This dataset contains records of individual taxi trips in New York City.

| Property | Value |
|----------|-------|
| Base URL | https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api |
| Format | Paginated JSON |
| Page Size | 1,000 records per page |
| Pagination | Stop when an empty page is returned |

## Setup Instructions

Since this API is custom (not one of the scaffolds in dlt workspace), the setup is slightly different.

### Step 1: Create a New Project (or Reuse Your Demo Project)

If you already created a project folder while following along with the workshop demo, you can reuse that folder. Otherwise, create a new one:

```bash
mkdir taxi-pipeline
cd taxi-pipeline
```

Open this folder in Cursor (or your preferred agentic IDE).

### Step 2: Set Up the dlt MCP Server (If Not Already Done)

Choose the setup for your IDE:

**Cursor** - Go to Settings → Tools & MCP → New MCP Server and add:

```json
{
  "mcpServers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}
```

**VS Code (Copilot)** - Create `.vscode/mcp.json` in your project folder:

```json
{
  "servers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}
```

**Claude Code** - Run in your terminal:

```bash
claude mcp add dlt -- uv run --with "dlt[duckdb]" --with "dlt-mcp[search]" python -m dlt_mcp
```

This enables the dlt MCP server, giving the AI access to dlt documentation, code examples, and your pipeline metadata.

### Step 3: Initialize uv

```bash
uv init
```

### Step 4: Install dlt

```bash
uv add "dlt[workspace]"
```

### Step 5: Initialize the Project

```bash
uv run dlt init dlthub:taxi_pipeline duckdb
```

You can name the project whatever you like. Since this API has no scaffold, the command will create:

- The dlt project files
- Cursor rules for AI assistance

But no YAML file with API metadata. You will need to provide the API information yourself.

### Step 6: Prompt the Agent

Now use your AI assistant to build the pipeline. You'll need to provide the API details in your prompt since there's no scaffold.

Here's an example to get you started:

```
Build a REST API source for NYC taxi data.

API details:
- Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Data format: Paginated JSON (1,000 records per page)
- Pagination: Stop when an empty page is returned

Place the code in taxi_pipeline.py and name the pipeline taxi_pipeline.
Use @dlt rest api as a tutorial.
```

### Step 7: Run and Debug

```bash
uv run taxi_pipeline.py
```

---

## Question 01

What is the start date and end date of the dataset?

- `2009-01-01` to `2009-01-31`
- `2009-06-01` to `2009-07-01`
- `2024-01-01` to `2024-02-01`
- `2024-06-01` to `2024-07-01`

### Solution

- Ask the agent to inspect the dataset and find the start and end dates.

- Possibly, it will execute the following query:

```sql
SELECT
  MIN(trip_pickup_date_time) AS start_date,
  MAX(trip_dropoff_date_time) AS end_date
FROM "taxi_rides";
```

**The correct answer is: `2009-06-01` to `2009-07-01`**

---

## Question 02

What proportion of trips are paid with credit card?

- 16.66%
- 26.66%
- 36.66%
- 46.66%

### Solution

- Ask the agent to inspect the dataset and find the proportion of trips paid with credit card.

- Possibly, it will execute the following query:

```sql
SELECT
  COUNT(1) / (SELECT COUNT(*) FROM "taxi_rides") * 100 AS credit_card_proportion
FROM "taxi_rides"
WHERE LOWER(payment_type) LIKE 'credit';
```

**The correct answer is: `26.66%`**

---

## Question 03

What is the total amount of money generated in tips?

- `$ 4,063.41`
- `$ 6,063.41`
- `$ 8,063.41`
- `$ 10,063.41`

### Solution

- Ask the agent to inspect the dataset and find the total amount of money generated in tips.

- Possibly, it will execute the following query:

```sql
SELECT
  ROUND(SUM(tip_amt), 2) AS total_tip_amount
FROM "taxi_rides";
```

**The correct answer is: `$6,063.41`**
