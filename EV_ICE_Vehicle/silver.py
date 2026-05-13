# Databricks notebook source
import pyspark.sql.functions as f



# COMMAND ----------

df = spark.read.table("ev_vs_ice_vehicle.bronze.ev_vs_ice_vehicle_specs_2015_2026")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Missing Values in Fuel_Type
# MAGIC
# MAGIC ### The Fuel_Type column contains missing values.

# COMMAND ----------

null_full_df = df.filter(f.col("Fuel_Type").isNull())
display(null_full_df)

# COMMAND ----------

df = df.withColumn(
    "Fuel_Type",
    f.when(f.col("Fuel_Type").isNull(), "Electric")
    .otherwise(f.col("Fuel_Type")),
)

display(df)

# COMMAND ----------

df.filter(f.col("Fuel_Type").isNull()).count()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. ICE Vehicles Having EV Range
# MAGIC
# MAGIC ### Some ICE vehicles contain non-zero values in EV_Range_miles.

# COMMAND ----------

invalid_ev_range = df.filter(
    (f.col("Vehicle_Category").contains("ICE")) &
    (f.col("EV_Range_miles")>0)
)

invalid_ev_range.display()

# COMMAND ----------

df = df.withColumn(
    "EV_Range_miles",
    f.when(
        f.col("Vehicle_Category").contains("ICE"),
        0
    ).otherwise(f.col("EV_Range_miles"))
    )

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Inconsistent Vehicle Categories
# MAGIC
# MAGIC ### Vehicle categories are inconsistent:

# COMMAND ----------

df = df.withColumn(
    "Vehicle_Category",
    f.when(f.col("Vehicle_Category").like("ICE%"),"ICE")
    .when(f.col("Vehicle_Category") == "EV", "EV")
    .otherwise("Hybrid")
)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Mixed Transmission Naming Conventions
# MAGIC
# MAGIC ### Transmission values are inconsistent.

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.withColumn(
    "Transmission_type",
    f.when(f.col("Transmission").contains("Automatic"), "Automatic")
    .when(f.col("Transmission").contains("Manual"), "Manual")
    .otherwise("Other")
)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Engine Columns Not Suitable for EVs
# MAGIC
# MAGIC ### EV vehicles may contain:
# MAGIC ### Engine_Cylinders = 0
# MAGIC ### Engine_Size_L = 0

# COMMAND ----------


display(df)

# COMMAND ----------

df = df.withColumn(
    "Engine_Size_L",
    f.when(f.col("Vehicle_Category") == "EV",
           None
    ).otherwise(f.col("Engine_Size_L")))
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. No Primary Key
# MAGIC
# MAGIC ### Dataset lacks a unique identifier.

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id

df = df.withColumn(
    "Vehicle_id",
    monotonically_increasing_id()
)

display(df)

# COMMAND ----------


df.write.mode("overwrite").saveAsTable("ev_vs_ice_vehicle.silver.vehicle_specs")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. High Cardinality in Model Column
# MAGIC
# MAGIC ### Model column contains many unique values.

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE ev_vs_ice_vehicle.silver.vehicle_specs
# MAGIC ZORDER BY (Make, Model)

# COMMAND ----------

df.write.mode("overwrite").saveAsTable("ev_vs_ice_vehicle.gold.gold_vehicle_specs")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ev_vs_ice_vehicle.gold.gold_vehicle_specs