SELECT
id,
name,
app,
project_id,
region,
IF(owners="", "System", owners) AS owners,
ready,
runnable,
completed,
interrupted,
start_timestamp,
end_timestamp,

TIMESTAMP_DIFF(TIMESTAMP_SECONDS(CAST(end_timestamp AS INT64)), TIMESTAMP_SECONDS(CAST(start_timestamp AS INT64)), SECOND) AS elapsed_timestamp_sec,
DATE(TIMESTAMP_SECONDS(CAST(start_timestamp AS INT64))) AS date

FROM (
  SELECT
  IF(ready_id IS NULL, interrupted_id,ready_id) AS id,
  IF(ready_name IS NULL, interrupted_name,ready_name) AS name,
  IF(ready_app IS NULL, interrupted_app,ready_app) AS app,
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
          ready_project_id,
          ready_region,
          ready_owners,

          ready_success,
          ready_acknowledge_timestamp,
          runnable_success,
          runnable_acknowledge_timestamp,
          runnable_processed_timestamp,
        FROM (
          SELECT
          id AS ready_id,
          name AS ready_name,
          app AS ready_app,
          project_id AS ready_project_id,
          region AS ready_region,
          owners AS ready_owners,
          #-----

          acknowledge_timestamp AS ready_acknowledge_timestamp,
          success AS ready_success
          FROM `<PROJECT_ID>.pulsar.ready_*`
          GROUP BY 1,2,3,4,5,6,7,8
        ) job_ready FULL JOIN (
          SELECT
          id AS runnable_id,
          acknowledge_timestamp AS runnable_acknowledge_timestamp,
          processed_timestamp AS runnable_processed_timestamp,
          success AS runnable_success
          FROM `<PROJECT_ID>.pulsar.runnable_*`
          GROUP BY 1,2,3,4
        ) job_runnable ON job_ready.ready_id=job_runnable.runnable_id
        GROUP BY 1,2,3,4,5,6,7,8,9,10,11
      ) ready_runnable FULL JOIN (
          SELECT
          id AS completed_id,
          processed_timestamp AS completed_processed_timestamp,
          success AS completed_success
          FROM `<PROJECT_ID>.pulsar.completed_*`
          GROUP BY 1,2,3
      ) completed ON ready_runnable.ready_id = completed_id
      GROUP BY 1,2,3,4,5,6,7,8,9,10,11, 12,13
    ) ready_runnable_completed FULL JOIN (
          SELECT
          id AS interrupted_id,
          name AS interrupted_name,
          state AS interrupted_state,
          app AS interrupted_app,
          project_id AS interrupted_project_id,
          region AS interrupted_region,
          owners AS interrupted_owners,
          #-----

          acknowledge_timestamp AS interrupted_acknowledge_timestamp,
          processed_timestamp AS interrupted_processed_timestamp,
          success AS interrupted_success
          FROM `<PROJECT_ID>.pulsar.interrupted_*`
          GROUP BY 1,2,3,4,5,6,7,8,9,10
    ) interrupted ON ready_runnable_completed.ready_id = interrupted.interrupted_id
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11, 12,13,14,15,16,17,18,19,20,21,22,23
  )
  GROUP BY 1,2,3,4,5,6,7,8,9,10,11, 12
)