# Databricks notebook source
df = spark.readStream.table("ev_vs_ice_vehicle.bronze.ev_vs_ice_vehicle_specs_2015_2026")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col

df = df\
    .withColumn("ingestion_time",current_timestamp())\
    .withColumn("source_file", col("_metadata.file_path"))

# COMMAND ----------

query = df.writeStream\
    .format("delta")\
    .outputMode("append")\
    .option("checkpointLocation", "/Workspace/Users/sarthak5634sharma@gmail.com/checkpoints/ev_vehicle_stream")\
    .trigger(once=True)\
    .toTable("ev_vs_ice_vehicle.bronze.ev_vs_ice_vehicle_stream")

query.awaitTermination()

# COMMAND ----------

