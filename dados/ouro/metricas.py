#%%
from dados.prata.silver import silver
import pyspark.sql
import pyspark.sql.functions as F

#%%
tabelao = silver()
df_obj = (
    tabelao
        .groupBy(['objective','device','region'])
        .agg(
        {'channel':"count"},
        {'impressions':"sum"},
        {'budget_daily':'sum'},
        {'clicks':'sum'},
        {'conversions':'sum'},
        {'revenue':'sum'})
        .withColumn("ctr",
        F.when(F.col("impressions") > 0, F.col("clicks") / F.col("impressions")))
               .withColumn("cpc",
                F.when(F.col("clicks") > 0, F.col("cost") / F.col("clicks")))
)