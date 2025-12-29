#%%
import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

def dadosbrutos(
    channel: str,
    start_date="2025-01-01",
    days=30,
    rows_per_day=10,
    output_path="dados/bronze"
):
    campaigns = [
        {"id": 1, "name": "Empresarial", "objective": "conversions"},
        {"id": 2, "name": "Condominio", "objective": "conversions"},
        {"id": 3, "name": "Office", "objective": "traffic"},
        {"id": 4, "name": "Apartamento", "objective": "conversions"},
        {"id": 5, "name": "Casa", "objective": "awareness"}
    ]

    ad_groups = ["Promo Janeiro", "IPTU 0", "Black Friday", "Lançamento", "Remarketing"]
    devices = ["mobile", "desktop"]
    regions = ["SE", "RN", "CE", "PE", "BA", "AL"]
    status_list = ["active"]

    channel_params = {
        "google_ads": {"impr": (500, 4000), "ctr": (0.02, 0.06), "conv": (0.03, 0.08), "ticket": (800, 2000)},
        "meta_ads": {"impr": (800, 6000), "ctr": (0.01, 0.04), "conv": (0.015, 0.05), "ticket": (700, 1800)},
        "email": {"impr": (200, 1500), "ctr": (0.10, 0.30), "conv": (0.02, 0.06), "ticket": (600, 1500)}
    }

    p = channel_params[channel]
    start = datetime.strptime(start_date, "%Y-%m-%d")
    rows = []

    for d in range(days):
        date = start + timedelta(days=d)

        for _ in range(rows_per_day):
            camp = random.choice(campaigns)
            impressions = random.randint(*p["impr"])
            clicks = max(0, int(impressions * random.uniform(*p["ctr"])))
            conversions = max(0, int(clicks * random.uniform(*p["conv"])))
            revenue = round(conversions * random.uniform(*p["ticket"]), 2)

            rows.append({
                "date": date.strftime("%Y-%m-%d"),
                "channel": channel,
                "platform": channel.split("_")[0],
                "campaign_id": camp["id"],
                "campaign": camp["name"],
                "objective": camp["objective"],
                "ad_group": random.choice(ad_groups),
                "creative_id": f"cr_{random.randint(1000,9999)}",
                "device": random.choice(devices),
                "region": random.choice(regions),
                "status": random.choice(status_list),
                "budget_daily": round(random.uniform(100, 2000), 2),
                "currency": "BRL",
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "revenue": revenue
            })

    df = pd.DataFrame(rows)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    file = f"{output_path}/{channel}_raw.csv"
    df.to_csv(file, index=False)
    print(f"✅ Gerado: {file} ({len(df)} linhas)")

dadosbrutos("google_ads")
dadosbrutos("meta_ads")
dadosbrutos("email")

# %%
