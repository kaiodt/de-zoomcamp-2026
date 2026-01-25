# Homework 01

## Question 01 - Understanding Docker images

Run docker with the `python:3.13 image`. Use an entrypoint bash to interact with the container.

What's the version of `pip` in the image?

### Solution

- Run the following command to start the container:

    ```bash
    docker run -it --rm --entrypoint bash python:3.13 
    ```

- Then, run the following command to check the version of `pip`:

    ```bash
    pip --version
    ```

- **The result is:**

    ```bash
    pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
    ```

## Question 02 - Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the hostname and port that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

### Solution

- **There are two possible answers:**

    - `postgres` and `5432`
    - `db` and `5432`


## Preparation for Questions 03 to 06

- First, rename the `.env.example` file to `.env` and check the variables. Adjust them as needed.

- Then, run the following command to build the ingestion script image:

    ```bash
    docker build -t ingest_data:v001 .
    ```

- Then, run the following command to start the PostgreSQL and pgadmin services:

    ```bash
    docker compose up -d
    ```

- When both services are up, run the following command to run the ingestion script:

    ```bash
    docker run -it --rm \
      --network pg-network \
      ingest_data:v001 \
      --year 2025 \
      --month 11
    ```

- When the script is done, open pgadmin, create a connection to the database (using the credentials in the `.env` file), and run the queries corresponding to each question.


## Question 03 - Counting short trips

For the trips in November 2025 (`lpep_pickup_datetime` between `2025-11-01` and `2025-12-01`, exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

### Solution

```sql
SELECT
  COUNT(1) AS "Num Trips"
FROM
  public.green_taxi_data
WHERE
  DATE_PART('YEAR', lpep_pickup_datetime) = 2025
  AND DATE_PART('MONTH', lpep_pickup_datetime) = 11
  AND trip_distance <= 1;
```

**The result is: `8,007`**


## Question 04 - Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

### Solution

```sql
SELECT
  CAST(lpep_pickup_datetime AS DATE) AS "Day",
  trip_distance AS "Longest Trip Distance"
FROM
  public.green_taxi_data
WHERE
  DATE_PART('YEAR', lpep_pickup_datetime) = 2025
  AND DATE_PART('MONTH', lpep_pickup_datetime) = 11
  AND trip_distance < 100
ORDER BY
  trip_distance DESC
LIMIT 1;
```

**The result is: `2025-11-14`**


## Question 05 - Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

### Solution

```sql
SELECT
  tz."Zone",
  SUM(td.total_amount) AS "Total Amount"
FROM
  public.green_taxi_data td
  JOIN public.taxi_zone_data tz
    ON td."PULocationID" = tz."LocationID"
WHERE
  CAST(td.lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY
  tz."Zone"
ORDER BY
  SUM(td.total_amount) DESC
LIMIT 1;
```

**The result is: `East Harlem North`**


## Question 06 - Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: It's tip , not trip. We need the name of the zone, not the ID.

### Solution

```sql
SELECT
  tzdo."Zone" AS "Dropoff Zone",
  td.tip_amount
FROM
  public.green_taxi_data td
  JOIN public.taxi_zone_data tzpu
    ON td."PULocationID" = tzpu."LocationID"
  JOIN public.taxi_zone_data tzdo
    ON td."DOLocationID" = tzdo."LocationID"
WHERE
  DATE_PART('YEAR', td.lpep_pickup_datetime) = 2025
  AND DATE_PART('MONTH', td.lpep_pickup_datetime) = 11
  AND tzpu."Zone" = 'East Harlem North'
ORDER BY
  td.tip_amount DESC
LIMIT 1;
```

**The result is: `Yorkville West`**


## Question 07 - Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

- Downloading the provider plugins and setting up backend
- Generating proposed changes and auto-executing the plan
- Remove all resources managed by terraform

### Solution

- `terraform init`
- `terraform apply -auto-approve`
- `terraform destroy`

