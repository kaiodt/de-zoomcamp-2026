SELECT
  td.tpep_pickup_datetime,
  td.tpep_dropoff_datetime,
  td.total_amount,
  CONCAT(tzpu."Borough", ' | ', tzpu."Zone") AS pickup_loc,
  CONCAT(tzdo."Borough", ' | ', tzdo."Zone") AS dropoff_loc
FROM
  public.yellow_taxi_data td
  JOIN public.taxi_zone_lookup tzpu
    ON td."PULocationID" = tzpu."LocationID"
  JOIN public.taxi_zone_lookup tzdo
    ON td."DOLocationID" = tzpu."LocationID"
LIMIT 100;

---

SELECT
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  public.yellow_taxi_data
WHERE
  "PULocationID" IS NULL
  OR "DOLocationID" IS NULL;

---

SELECT
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  public.yellow_taxi_data
WHERE
  "PULocationID" NOT IN (
    SELECT "LocationID"
    FROM public.taxi_zone_lookup
   )
  OR "DOLocationID" NOT IN (
    SELECT "LocationID"
    FROM public.taxi_zone_lookup
   );

---

SELECT
  td.tpep_pickup_datetime,
  td.tpep_dropoff_datetime,
  td.total_amount,
  COALESCE(
    CONCAT(tzpu."Borough", ' | ', tzpu."Zone"),
    'Unknown | Unknown'
  ) AS pickup_loc,
  COALESCE(
    CONCAT(tzdo."Borough", ' | ', tzdo."Zone"),
    'Unknown | Unknown'
  ) AS dropoff_loc
FROM
  public.yellow_taxi_data td
  LEFT JOIN public.taxi_zone_lookup tzpu
    ON td."PULocationID" = tzpu."LocationID"
  LEFT JOIN public.taxi_zone_lookup tzdo
    ON td."DOLocationID" = tzdo."LocationID"
LIMIT 100;

---

SELECT
  CAST(tpep_pickup_datetime AS DATE) AS "Day",
  COUNT(1) AS "Num Trips"
FROM
  public.yellow_taxi_data
WHERE
  DATE_PART('YEAR', tpep_pickup_datetime) = 2021
  AND DATE_PART('MONTH', tpep_pickup_datetime) = 1
GROUP BY
  CAST(tpep_pickup_datetime AS DATE)
ORDER BY
  "Day";

---

SELECT
  CAST(td.tpep_pickup_datetime AS DATE) AS "Day",
  CONCAT(tz."Borough", ' | ', tz."Zone") AS "Pickup",
  COUNT(1) AS "Num Trips",
  CEIL(AVG(td.passenger_count)) AS "Avg. Passangers",
  ROUND(AVG(td.total_amount)::NUMERIC, 2) AS "Avg. Amount"
FROM
  public.yellow_taxi_data td
  JOIN public.taxi_zone_lookup tz
    ON td."PULocationID" = tz."LocationID"
WHERE
  DATE_PART('YEAR', td.tpep_pickup_datetime) = 2021
  AND DATE_PART('MONTH', td.tpep_pickup_datetime) = 1
GROUP BY
  CAST(td.tpep_pickup_datetime AS DATE),
  CONCAT(tz."Borough", ' | ', tz."Zone")
ORDER BY
  "Day", "Pickup";
