# -------------------------------------------------- YOU CAN UPDATE THIS LIST WITH NEW TYPE OF INSTANCES --------------------------------------------
WITH pricing AS (
  SELECT [
    STRUCT("128" AS pricing_memory,"0.083" AS virtual_cpu, "0.000000231" AS pricing_tier_one, "0.000000324" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("256" AS pricing_memory,"0.167" AS virtual_cpu, "0.000000463" AS pricing_tier_one, "0.000000648" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("512" AS pricing_memory,"0.333" AS virtual_cpu, "0.000000925" AS pricing_tier_one, "0.000001295" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("1024" AS pricing_memory,"0.583" AS virtual_cpu, "0.000001650" AS pricing_tier_one, "0.000002310" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("2048" AS pricing_memory,"1" AS virtual_cpu, "0.000002900" AS pricing_tier_one, "0.000004060" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("4096" AS pricing_memory,"2" AS virtual_cpu, "0.000005800" AS pricing_tier_one, "0.000008120" AS pricing_tier_two, "100" AS pricing_ms),
    STRUCT("8192" AS pricing_memory,"2" AS virtual_cpu, "0.000006800" AS pricing_tier_one, "0.000009520" AS pricing_tier_two, "100" AS pricing_ms)
    ] AS details
)
#----------------------------------------------------------------------------------------------------------------------------------------------------
SELECT
id,
name,
project_id,
app,
CAST(memory AS FLOAT64) AS memory,
CAST(virtual_cpu AS FLOAT64) AS virtual_cpu,
(CAST(processing.elapsed_timestamp_msec AS FLOAT64) * CAST(pricing_tier_one AS FLOAT64))/CAST(pricing_ms AS FLOAT64) AS cost,
region,
owners,
CAST(ready AS INT64) AS ready,
CAST(runnable AS INT64) AS runnable,
CAST(completed AS INT64) AS completed,
CAST(interrupted AS INT64) AS interrupted,
start_timestamp,
end_timestamp,
elapsed_timestamp_msec,
date
FROM (
  SELECT
  id,
  name,
  app,
  REPLACE(LOWER(memory), "m", "") AS memory,
  project_id,
  region,
  IF(owners="", "System", owners) AS owners,
  ready,
  runnable,
  completed,
  interrupted,
  start_timestamp,
  end_timestamp,

  TIMESTAMP_DIFF(TIMESTAMP_SECONDS(CAST(end_timestamp AS INT64)), TIMESTAMP_SECONDS(CAST(start_timestamp AS INT64)), MILLISECOND) AS elapsed_timestamp_msec,
  DATE(TIMESTAMP_SECONDS(CAST(start_timestamp AS INT64))) AS date

  FROM (
    SELECT
    IF(ready_id IS NULL, interrupted_id,ready_id) AS id,
    IF(ready_name IS NULL, interrupted_name,ready_name) AS name,
    IF(ready_app IS NULL, interrupted_app,ready_app) AS app,
    IF(ready_memory IS NULL, interrupted_memory,ready_memory) AS memory,
    IF(ready_project_id IS NULL, interrupted_project_id,ready_project_id) AS project_id,
    IF(ready_region IS NULL, interrupted_region,ready_region) AS region,
    IF(ready_owners IS NULL, interrupted_owners,ready_owners) AS owners,

    IF(ready_success = "True", 1, 0) AS ready,
    IF(runnable_success = "True", 1, 0) AS runnable,
    IF(completed_success = "True", 1, 0) AS completed,
    IF(interrupted_success = "False", 1, 0) AS interrupted,

    # Find start time
    # It is a ready task or interrupted task acknowledge time
    CASE
      WHEN (interrupted_acknowledge_timestamp IS NOT NULL AND ready_acknowledge_timestamp IS NULL) THEN interrupted_acknowledge_timestamp
      WHEN ready_acknowledge_timestamp IS NOT NULL THEN ready_acknowledge_timestamp
      WHEN runnable_acknowledge_timestamp IS NOT NULL THEN runnable_acknowledge_timestamp
    END AS start_timestamp,

    # Find end time
    # It is a completed task or interrupted processed time
    CASE
      WHEN completed_processed_timestamp IS NOT NULL THEN completed_processed_timestamp
      WHEN interrupted_processed_timestamp IS NOT NULL THEN interrupted_processed_timestamp
    END AS end_timestamp

    FROM (
      SELECT
      *
      FROM (
        SELECT
            ready_id,
            ready_name,
            ready_app,
            ready_memory,
            ready_project_id,
            ready_region,
            ready_owners,

            ready_success,
            ready_acknowledge_timestamp,
            runnable_success,
            runnable_acknowledge_timestamp,
            runnable_processed_timestamp,
            completed_success,
            completed_processed_timestamp
        FROM (
          SELECT
            ready_id,
            ready_name,
            ready_app,
            ready_memory,
            ready_project_id,
            ready_region,
            ready_owners,

            ready_success,
            ready_acknowledge_timestamp,
            runnable_success,
            runnable_acknowledge_timestamp,
            runnable_processed_timestamp
          FROM (
            SELECT
            id AS ready_id,
            name AS ready_name,
            app AS ready_app,
            memory AS ready_memory,
            project_id AS ready_project_id,
            region AS ready_region,
            owners AS ready_owners,
            #-----

            acknowledge_timestamp AS ready_acknowledge_timestamp,
            success AS ready_success
            FROM `@PROJECT_ID.@DATASET_ID.ready_*`
            GROUP BY 1,2,3,4,5,6,7,8,9
          ) job_ready FULL JOIN (
            SELECT
            id AS runnable_id,
            acknowledge_timestamp AS runnable_acknowledge_timestamp,
            processed_timestamp AS runnable_processed_timestamp,
            success AS runnable_success
            FROM `@PROJECT_ID.@DATASET_ID.runnable_*`
            GROUP BY 1,2,3,4
          ) job_runnable ON job_ready.ready_id=job_runnable.runnable_id
          GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12
        ) ready_runnable FULL JOIN (
            SELECT
            id AS completed_id,
            processed_timestamp AS completed_processed_timestamp,
            success AS completed_success
            FROM `@PROJECT_ID.@DATASET_ID.completed_*`
            GROUP BY 1,2,3
        ) completed ON ready_runnable.ready_id = completed_id
        GROUP BY 1,2,3,4,5,6,7,8,9,10,11, 12,13, 14
      ) ready_runnable_completed FULL JOIN (
            SELECT
            id AS interrupted_id,
            name AS interrupted_name,
            state AS interrupted_state,
            app AS interrupted_app,
            memory AS interrupted_memory,
            project_id AS interrupted_project_id,
            region AS interrupted_region,
            owners AS interrupted_owners,
            #-----

            acknowledge_timestamp AS interrupted_acknowledge_timestamp,
            processed_timestamp AS interrupted_processed_timestamp,
            success AS interrupted_success
            FROM `@PROJECT_ID.@DATASET_ID.interrupted_*`
            GROUP BY 1,2,3,4,5,6,7,8,9,10,11
      ) interrupted ON ready_runnable_completed.ready_id = interrupted.interrupted_id
      GROUP BY 1,2,3,4,5,6,7,8,9,10,11, 12,13,14,15,16,17,18,19,20,21,22,23,24,25
    )
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13
  )
) processing LEFT JOIN (
  SELECT
  *
  FROM(
    SELECT
    pricing_details.pricing_memory,
    pricing_details.virtual_cpu,
    pricing_details.pricing_tier_one,
    pricing_details.pricing_tier_two,
    pricing_details.pricing_ms
    FROM pricing, UNNEST(details) AS pricing_details
  ) GROUP BY 1,2,3,4,5
) pricing ON processing.memory = pricing.pricing_memory