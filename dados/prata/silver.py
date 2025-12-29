#%%
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
#%%
RAW_PATH = "dados/bronze"
OUTPUT_PATH = "dados/ouro/campaigns_final"

def silver():
    spark = (
        SparkSession
        .builder
        .master("local[*]")
        .appName("MarketingPipeline")
        .getOrCreate()
    )

    sources = ["google_ads_raw", "meta_ads_raw", "email_raw"]
    dfs = []

    for src in sources:
        df = (
            spark.read
            .option("header", True)
            .csv(f"{RAW_PATH}{src}.csv")
            .withColumn("source", F.lit(src))
        )
        dfs.append(df)

    df_all = dfs[0]
    for df in dfs[1:]:
        df_all = df_all.unionByName(df)

    df_all = (
        df_all
        .withColumn("date", F.to_date("date"))
        .withColumn("impressions", F.col("impressions").cast("long"))
        .withColumn("clicks", F.col("clicks").cast("long"))
        .withColumn("cost", F.col("cost").cast("double"))
        .withColumn("conversions", F.col("conversions").cast("long"))
        .withColumn("revenue", F.col("revenue").cast("double"))
    )

    df_all = (
        df_all
        .withColumn("ctr",
            F.when(F.col("impressions") > 0, F.col("clicks") / F.col("impressions"))
        )
        .withColumn("cpc",
            F.when(F.col("clicks") > 0, F.col("cost") / F.col("clicks"))
        )
    )

    (
        df_all
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(OUTPUT_PATH)
    )

    print("✅ Pipeline finalizado com sucesso")
    spark.stop()


# %%
spark = (
        SparkSession
        .builder
        .master("local[*]")
        .appName("MarketingPipeline")
        .getOrCreate()
    )
caminho = 'c:/Users/Pedro/Documents/vscode/pipeline_dados/dados/bronze/'
meta_ads = (spark.read
      .option("header", True)
      .csv(f'{caminho}meta_ads_raw.csv'))
email = spark.read.option('header',True).csv(f'{caminho}email_raw.csv')