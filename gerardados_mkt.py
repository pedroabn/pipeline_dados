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
        {"id": 1, "name": "CPU", "objective": "conversions"},
        {"id": 2, "name": "Memoria RAM", "objective": "conversions"},
        {"id": 3, "name": "Placa de vídeo", "objective": "traffic"},
        {"id": 4, "name": "Monitor", "objective": "conversions"},
        {"id": 5, "name": "Periféricos", "objective": "awareness"}
    ]

    ad_groups = ["Promo Janeiro", "Imposto 0", "Black Friday", "Lançamento", "Remarketing"]
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
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações
np.random.seed(42)
random.seed(42)

# Período da campanha
dias_campanha = 30
data_inicio = datetime.now() - timedelta(days=dias_campanha)

# Produtos da loja de hardware
produtos = [
    'Teclado Mecânico',
    'Mouse Gamer',
    'Headset',
    'Webcam',
    'Mousepad',
    'Monitor',
    'Cadeira Gamer',
    'Microfone',
    'GPU RTX',
    'Processador',
    'Memória RAM',
    'SSD'
]

cidades_brasil = [
    'São Paulo', 'Rio de Janeiro', 'Brasília', 'Belo Horizonte',
    'Curitiba', 'Porto Alegre', 'Recife', 'Salvador', 
    'Fortaleza', 'Manaus', 'Goiânia', 'Belém'
]

def gerar_dados_ga4(num_registros=500):
    """
    Gera dados do Google Analytics 4
    Fontes: email, site (direto), SEO (orgânico)
    """
    dados = []
    
    for _ in range(num_registros):
        # Data aleatória dentro do período
        data = data_inicio + timedelta(days=random.randint(0, dias_campanha))
        
        # Definir fonte e medium
        fonte_tipo = random.choices(
            ['seo', 'email', 'direto'],
            weights=[45, 30, 25]  # SEO é a principal fonte
        )[0]
        
        if fonte_tipo == 'seo':
            source = random.choice(['google', 'bing', 'yahoo'])
            medium = 'organic'
            # SEO: bom engajamento, conversão média
            sessions = random.randint(30, 150)
            bounce_rate = random.uniform(0.35, 0.55)
            avg_session_duration = random.uniform(120, 300)
            conversion_rate = random.uniform(0.02, 0.05)
            
        elif fonte_tipo == 'email':
            source = 'newsletter'
            medium = 'email'
            # Email: melhor conversão, engajamento alto
            sessions = random.randint(50, 200)
            bounce_rate = random.uniform(0.20, 0.40)
            avg_session_duration = random.uniform(150, 350)
            conversion_rate = random.uniform(0.04, 0.08)
            
        else:  # direto
            source = '(direct)'
            medium = '(none)'
            # Direto: usuários conhecem a marca, boa conversão
            sessions = random.randint(40, 180)
            bounce_rate = random.uniform(0.25, 0.45)
            avg_session_duration = random.uniform(130, 280)
            conversion_rate = random.uniform(0.03, 0.06)
        
        # Dispositivo
        device = random.choices(
            ['desktop', 'mobile', 'tablet'],
            weights=[60, 35, 5]  # Hardware PC = mais desktop
        )[0]
        
        # Calcular métricas
        total_users = int(sessions * random.uniform(0.75, 0.90))
        new_users = int(total_users * random.uniform(0.55, 0.80))
        page_views = int(sessions * random.uniform(2.5, 6.0))
        conversions = int(sessions * conversion_rate)
        engagement_rate = 1 - bounce_rate
        
        # Valor médio do pedido para hardware
        avg_order_value = random.uniform(150, 800)
        revenue = conversions * avg_order_value
        
        # Produto mais visualizado
        produto = random.choice(produtos)
        
        dados.append({
            'date': data.strftime('%Y-%m-%d'),
            'session_source': source,
            'session_medium': medium,
            'device_category': device,
            'city': random.choice(cidades_brasil),
            'sessions': sessions,
            'total_users': total_users,
            'new_users': new_users,
            'page_views': page_views,
            'conversions': conversions,
            'avg_session_duration_seconds': round(avg_session_duration, 2),
            'bounce_rate': round(bounce_rate, 4),
            'engagement_rate': round(engagement_rate, 4),
            'revenue': round(revenue, 2),
            'avg_order_value': round(avg_order_value, 2),
            'top_product': produto
        })
    
    return pd.DataFrame(dados)


def gerar_dados_meta_ads(num_campanhas=30):
    """
    Gera dados do Meta Ads (Facebook e Instagram)
    """
    dados = []
    
    tipos_campanha = [
        'Conversão - Teclados Mecânicos',
        'Tráfego - Mouses Gamer',
        'Alcance - Headsets',
        'Engajamento - Periféricos RGB',
        'Remarketing - Carrinho Abandonado',
        'Vendas - Black Friday Hardware',
        'Cadastro - Newsletter Tech',
        'Conversão - Monitores',
        'Tráfego - Setup Gamer',
        'Vendas - Componentes PC'
    ]
    
    for i in range(num_campanhas):
        # Plataforma (Facebook ou Instagram)
        platform = random.choice(['Facebook', 'Instagram'])
        
        # Nome da campanha
        campaign_name = random.choice(tipos_campanha)
        
        # Objetivo da campanha
        if 'Conversão' in campaign_name or 'Vendas' in campaign_name:
            objective = 'CONVERSIONS'
            # Campanhas de conversão: maior investimento, melhor ROAS
            spend = random.uniform(1000, 5000)
            conversion_rate = random.uniform(0.025, 0.06)
            cpc = random.uniform(0.80, 2.50)
        elif 'Tráfego' in campaign_name:
            objective = 'TRAFFIC'
            spend = random.uniform(500, 2000)
            conversion_rate = random.uniform(0.015, 0.035)
            cpc = random.uniform(0.50, 1.80)
        elif 'Alcance' in campaign_name:
            objective = 'REACH'
            spend = random.uniform(300, 1500)
            conversion_rate = random.uniform(0.008, 0.020)
            cpc = random.uniform(0.30, 1.20)
        elif 'Remarketing' in campaign_name:
            objective = 'CONVERSIONS'
            # Remarketing: alta conversão, menor CPC
            spend = random.uniform(800, 3000)
            conversion_rate = random.uniform(0.045, 0.10)
            cpc = random.uniform(0.60, 1.80)
        else:  # Engajamento, Cadastro
            objective = 'ENGAGEMENT'
            spend = random.uniform(400, 1800)
            conversion_rate = random.uniform(0.012, 0.030)
            cpc = random.uniform(0.40, 1.50)
        
        # Instagram geralmente tem CPC menor mas conversão também menor
        if platform == 'Instagram':
            cpc *= 0.85
            conversion_rate *= 0.90
        
        # Calcular métricas
        impressions = int(spend / cpc * random.uniform(800, 1200))
        clicks = int(impressions * random.uniform(0.008, 0.025))
        conversions = int(clicks * conversion_rate)
        
        # Alcance e frequência
        reach = int(impressions * random.uniform(0.60, 0.85))
        frequency = impressions / reach if reach > 0 else 1
        
        # Público-alvo
        age_min = random.choice([18, 25, 30, 35])
        age_max = age_min + random.choice([10,12,14,15,16,32,21,20])
        gender = random.choice(['Todos', 'Masculino', 'Feminino'])
        
        # Produto da campanha
        produto = random.choice(produtos)
        
        dados.append({
            'campaign_id': f'camp_{23847000000 + i}',
            'campaign_name': f'{campaign_name} - {platform}',
            'platform': platform,
            'objective': objective,
            'status': random.choices(['ACTIVE', 'PAUSED'], weights=[85, 15])[0],
            'date_start': (data_inicio + timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d'),
            'date_stop': (data_inicio + timedelta(days=dias_campanha)).strftime('%Y-%m-%d'),
            'impressions': impressions,
            'reach': reach,
            'frequency': round(frequency, 2),
            'clicks': clicks,
            'ctr': round(ctr, 2),
            'cpc': round(cpc_real, 2),
            'cpm': round(cpm, 2),
            'spend': round(spend, 2),
            'conversions': conversions,
            'cost_per_conversion': round(cost_per_conversion, 2),
            'revenue': round(revenue, 2),
            'roas': round(roas, 2),
            'avg_order_value': round(avg_order_value, 2),
            'age_min': age_min,
            'age_max': age_max,
            'gender': gender,
            'location': 'Brasil',
            'product': produto
        })
    
    return pd.DataFrame(dados)


# Gerar os dados
print("Gerando dados do GA4...")
df_ga4 = gerar_dados_ga4(num_registros=800)

print("Gerando dados do Meta Ads...")
df_meta = gerar_dados_meta_ads(num_campanhas=15)

# Salvar em Parquet
print("\nSalvando arquivos Parquet...")
df_ga4.to_parquet('ga4_hardware_campaign.parquet', index=False, engine='pyarrow')
df_meta.to_parquet('meta_ads_hardware_campaign.parquet', index=False, engine='pyarrow')