/* @bruin
name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: date
  time_granularity: date

columns:
  - name: date
    type: date
    description: Trip date (derived from pickup_datetime)
    checks:
      - name: not_null

  - name: taxi_type
    type: string
    description: Type of taxi (yellow/green)
    checks:
      - name: not_null

  - name: payment_type_name
    type: string
    description: Payment method name

  - name: total_trips
    type: integer
    description: Total number of trips
    checks:
      - name: positive

  - name: total_passengers
    type: integer
    description: Total number of passengers
    checks:
      - name: non_negative

  - name: avg_passengers
    type: float
    description: Average number of passengers
    checks:
      - name: non_negative

  - name: total_revenue
    type: float
    description: Total revenue
    checks:
      - name: non_negative

  - name: avg_revenue
    type: float
    description: Average revenue per trip
    checks:
      - name: non_negative

  - name: total_fare
    type: float
    description: Total fare amount
    checks:
      - name: non_negative

  - name: avg_fare
    type: float
    description: Average fare amount
    checks:
      - name: non_negative

  - name: total_tip
    type: float
    description: Total tip amount
    checks:
      - name: non_negative

  - name: avg_tip
    type: float
    description: Average tip amount
    checks:
      - name: non_negative

  - name: total_distance
    type: float
    description: Total trip distance
    checks:
      - name: non_negative

  - name: avg_distance
    type: float
    description: Average trip distance
    checks:
      - name: non_negative

  - name: total_duration_minutes
    type: float
    description: Total trip duration in minutes
    checks:
      - name: non_negative

  - name: avg_trip_duration_minutes
    type: float
    description: Average trip duration in minutes
    checks:
      - name: non_negative

@bruin */

SELECT
  DATE_TRUNC('day', pickup_datetime)::date AS date,
  taxi_type,
  payment_type_name,

  COUNT(*) AS total_trips,

  SUM(passenger_count) AS total_passengers,
  AVG(passenger_count) AS avg_passengers,

  SUM(total_amount) AS total_revenue,
  AVG(total_amount) AS avg_revenue,

  SUM(fare_amount) AS total_fare,
  AVG(fare_amount) AS avg_fare,

  SUM(tip_amount) AS total_tip,
  AVG(tip_amount) AS avg_tip,

  SUM(trip_distance) AS total_distance,
  AVG(trip_distance) AS avg_distance,

  SUM(
    DATE_DIFF('minute', pickup_datetime, dropoff_datetime)
  ) AS total_duration_minutes,
  AVG(
    DATE_DIFF('minute', pickup_datetime, dropoff_datetime)
  ) AS avg_trip_duration_minutes

FROM
  staging.trips

WHERE
  pickup_datetime >= '{{ start_date }}'
  AND pickup_datetime < '{{ end_date }}'
  AND DATE_DIFF('minute', pickup_datetime, dropoff_datetime) >= 0
  AND fare_amount >= 0
  AND total_amount >= 0

GROUP BY
  date,
  taxi_type,
  payment_type_name
