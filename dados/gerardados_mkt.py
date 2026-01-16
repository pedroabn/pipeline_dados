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
    'Teclado Mecânico RGB',
    'Mouse Gamer 16000 DPI',
    'Headset 7.1 Surround',
    'Webcam Full HD',
    'Mousepad Gamer XXL',
    'Monitor 144Hz',
    'Cadeira Gamer Pro',
    'Microfone Condensador',
    'GPU RTX 4060',
    'Processador AMD Ryzen',
    'Memória RAM 16GB',
    'SSD NVMe 1TB'
]

categorias = {
    'Teclado Mecânico RGB': 'Teclados',
    'Mouse Gamer 16000 DPI': 'Mouses',
    'Headset 7.1 Surround': 'Audio',
    'Webcam Full HD': 'Periféricos',
    'Mousepad Gamer XXL': 'Acessórios',
    'Monitor 144Hz': 'Monitores',
    'Cadeira Gamer Pro': 'Mobiliário',
    'Microfone Condensador': 'Audio',
    'GPU RTX 4060': 'Componentes',
    'Processador AMD Ryzen': 'Componentes',
    'Memória RAM 16GB': 'Componentes',
    'SSD NVMe 1TB': 'Armazenamento'
}

precos = {
    'Teclado Mecânico RGB': 459.90,
    'Mouse Gamer 16000 DPI': 189.90,
    'Headset 7.1 Surround': 349.90,
    'Webcam Full HD': 279.90,
    'Mousepad Gamer XXL': 79.90,
    'Monitor 144Hz': 1299.90,
    'Cadeira Gamer Pro': 899.90,
    'Microfone Condensador': 549.90,
    'GPU RTX 4060': 2499.90,
    'Processador AMD Ryzen': 1199.90,
    'Memória RAM 16GB': 299.90,
    'SSD NVMe 1TB': 399.90
}

cidades_brasil = [
    'São Paulo', 'Rio de Janeiro', 'Brasília', 'Belo Horizonte',
    'Curitiba', 'Porto Alegre', 'Recife', 'Salvador', 
    'Fortaleza', 'Manaus', 'Goiânia', 'Belém'
]

def gerar_user_id():
    """Gera um user_id único"""
    return f"user_{random.randint(100000, 999999)}"

def gerar_session_id():
    """Gera um session_id único"""
    return f"session_{random.randint(1000000000, 9999999999)}"

def gerar_dados_ga4_eventos(num_eventos=5000):
    """
    Gera dados BRUTOS de eventos do GA4
    Cada linha é um evento individual
    """
    eventos = []
    
    event_types = [
        'session_start',
        'page_view', 
        'view_item',
        'add_to_cart',
        'begin_checkout',
        'purchase',
        'scroll',
        'click'
    ]
    
    paginas = [
        '/',
        '/produtos',
        '/teclados-mecanicos',
        '/mouses-gamer',
        '/headsets',
        '/monitores',
        '/componentes-pc',
        '/carrinho',
        '/checkout',
        '/confirmacao-pedido',
        '/sobre',
        '/contato'
    ]
    
    for _ in range(num_eventos):
        # Data e hora do evento
        data = data_inicio + timedelta(
            days=random.randint(0, dias_campanha),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # Fonte de tráfego
        fonte_tipo = random.choices(
            ['seo', 'email', 'direto'],
            weights=[45, 30, 25]
        )[0]
        
        if fonte_tipo == 'seo':
            source = random.choice(['google', 'bing'])
            medium = 'organic'
            campaign = '(organic)'
        elif fonte_tipo == 'email':
            source = 'newsletter'
            medium = 'email'
            campaign = random.choice([
                'lancamento_perifericos',
                'black_friday_hardware',
                'oferta_teclados',
                'novos_monitores'
            ])
        else:
            source = '(direct)'
            medium = '(none)'
            campaign = '(direct)'
        
        # Tipo de evento
        event_name = random.choices(
            event_types,
            weights=[5, 30, 15, 10, 5, 3, 20, 12]
        )[0]
        
        # Dispositivo
        device = random.choices(
            ['desktop', 'mobile', 'tablet'],
            weights=[60, 35, 5]
        )[0]
        
        browser = random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'])
        os = random.choice(['Windows', 'macOS', 'Android', 'iOS'])
        
        # User e session
        user_id = gerar_user_id()
        session_id = gerar_session_id()
        
        # Dados do evento
        evento = {
            'event_date': data.strftime('%Y%m%d'),
            'event_timestamp': int(data.timestamp() * 1000000),  # microsegundos
            'event_name': event_name,
            'user_id': user_id,
            'session_id': session_id,
            'user_pseudo_id': f"pseudo_{random.randint(1000000, 9999999)}",
            'platform': 'WEB',
            'stream_id': '3847562910',
            'geo_country': 'Brazil',
            'geo_city': random.choice(cidades_brasil),
            'device_category': device,
            'device_operating_system': os,
            'device_browser': browser,
            'traffic_source_source': source,
            'traffic_source_medium': medium,
            'traffic_source_name': campaign,
            'page_location': f"https://hardwarestore.com.br{random.choice(paginas)}",
            'page_title': None,
            'engagement_time_msec': random.randint(0, 300000) if event_name != 'session_start' else 0,
        }
        
        # Parâmetros específicos por tipo de evento
        if event_name == 'view_item':
            produto = random.choice(produtos)
            evento['item_name'] = produto
            evento['item_category'] = categorias[produto]
            evento['price'] = precos[produto]
            evento['quantity'] = None
            
        elif event_name == 'add_to_cart':
            produto = random.choice(produtos)
            quantidade = random.randint(1, 3)
            evento['item_name'] = produto
            evento['item_category'] = categorias[produto]
            evento['price'] = precos[produto]
            evento['quantity'] = quantidade
            evento['value'] = precos[produto] * quantidade
            
        elif event_name == 'purchase':
            # Compra pode ter múltiplos itens
            num_itens = random.randint(1, 4)
            itens_compra = random.sample(produtos, min(num_itens, len(produtos)))
            
            valor_total = sum(precos[item] for item in itens_compra)
            evento['transaction_id'] = f"T{random.randint(100000, 999999)}"
            evento['value'] = valor_total
            evento['tax'] = valor_total * 0.12  # 12% de impostos
            evento['shipping'] = random.choice([0, 15.90, 29.90])
            evento['currency'] = 'BRL'
            evento['items_purchased'] = ','.join(itens_compra)
            evento['quantity'] = len(itens_compra)
        else:
            evento['item_name'] = None
            evento['item_category'] = None
            evento['price'] = None
            evento['quantity'] = None
        
        eventos.append(evento)
    
    return pd.DataFrame(eventos)


def gerar_dados_meta_ads_raw(dias=30):
    """
    Gera dados BRUTOS do Meta Ads
    Dados diários por campanha/ad set
    """
    dados = []
    
    campanhas = [
        {'id': 'camp_001', 'name': 'Conversão - Teclados Mecânicos', 'platform': 'Facebook', 'objective': 'CONVERSIONS'},
        {'id': 'camp_002', 'name': 'Conversão - Teclados Mecânicos', 'platform': 'Instagram', 'objective': 'CONVERSIONS'},
        {'id': 'camp_003', 'name': 'Tráfego - Mouses Gamer', 'platform': 'Facebook', 'objective': 'TRAFFIC'},
        {'id': 'camp_004', 'name': 'Tráfego - Mouses Gamer', 'platform': 'Instagram', 'objective': 'TRAFFIC'},
        {'id': 'camp_005', 'name': 'Alcance - Headsets Premium', 'platform': 'Facebook', 'objective': 'REACH'},
        {'id': 'camp_006', 'name': 'Alcance - Headsets Premium', 'platform': 'Instagram', 'objective': 'REACH'},
        {'id': 'camp_007', 'name': 'Remarketing - Carrinho Abandonado', 'platform': 'Facebook', 'objective': 'CONVERSIONS'},
        {'id': 'camp_008', 'name': 'Remarketing - Carrinho Abandonado', 'platform': 'Instagram', 'objective': 'CONVERSIONS'},
        {'id': 'camp_009', 'name': 'Vendas - Black Friday Hardware', 'platform': 'Facebook', 'objective': 'CONVERSIONS'},
        {'id': 'camp_010', 'name': 'Vendas - Black Friday Hardware', 'platform': 'Instagram', 'objective': 'CONVERSIONS'},
    ]
    
    ad_sets = [
        {'id': 'adset_001', 'name': 'Público Geral 18-35', 'age_min': 18, 'age_max': 35},
        {'id': 'adset_002', 'name': 'Público Gamer 25-45', 'age_min': 25, 'age_max': 45},
        {'id': 'adset_003', 'name': 'Entusiastas PC 30-50', 'age_min': 30, 'age_max': 50},
    ]
    
    for dia in range(dias):
        data = (data_inicio + timedelta(days=dia)).strftime('%Y-%m-%d')
        
        for campanha in campanhas:
            for adset in ad_sets:
                # Cada linha é um dia de uma combinação campanha + ad set
                
                # Variar métricas por tipo de campanha
                if campanha['objective'] == 'CONVERSIONS':
                    impressions = random.randint(5000, 25000)
                    ctr_base = random.uniform(0.015, 0.030)
                elif campanha['objective'] == 'TRAFFIC':
                    impressions = random.randint(8000, 35000)
                    ctr_base = random.uniform(0.018, 0.035)
                else:  # REACH
                    impressions = random.randint(15000, 50000)
                    ctr_base = random.uniform(0.008, 0.018)
                
                # Instagram tem CTR ligeiramente menor
                if campanha['platform'] == 'Instagram':
                    ctr_base *= 0.92
                
                clicks = int(impressions * ctr_base)
                reach = int(impressions * random.uniform(0.65, 0.85))
                spend = impressions * random.uniform(0.008, 0.025)
                
                # Algumas linhas podem ter conversões
                conversions = 0
                conversion_value = 0
                
                if random.random() < 0.40:  # 40% das linhas têm conversões
                    if campanha['objective'] == 'CONVERSIONS':
                        conversions = random.randint(1, 15)
                    elif campanha['objective'] == 'TRAFFIC':
                        conversions = random.randint(0, 8)
                    else:
                        conversions = random.randint(0, 3)
                    
                    # Valor das conversões
                    if conversions > 0:
                        conversion_value = sum(random.choice(list(precos.values())) 
                                              for _ in range(conversions))
                
                dados.append({
                    'date': data,
                    'campaign_id': campanha['id'],
                    'campaign_name': campanha['name'],
                    'ad_set_id': adset['id'],
                    'ad_set_name': adset['name'],
                    'platform': campanha['platform'],
                    'objective': campanha['objective'],
                    'impressions': impressions,
                    'reach': reach,
                    'clicks': clicks,
                    'spend': round(spend, 2),
                    'conversions': conversions,
                    'conversion_value': round(conversion_value, 2),
                    'age_min': adset['age_min'],
                    'age_max': adset['age_max'],
                    'gender': random.choice(['ALL', 'MALE', 'FEMALE']),
                    'placement': random.choice(['Feed', 'Stories', 'Reels', 'Marketplace']),
                    'country': 'BR',
                })
    
    return pd.DataFrame(dados)


# Gerar os dados
print("Gerando eventos brutos do GA4...")
df_ga4 = gerar_dados_ga4_eventos(num_eventos=5000)

print("Gerando dados brutos do Meta Ads...")
df_meta = gerar_dados_meta_ads_raw(dias=30)

# Salvar em Parquet
print("\nSalvando arquivos Parquet...")
df_ga4.to_parquet('ga4_events_raw.parquet', index=False, engine='pyarrow')
df_meta.to_parquet('meta_ads_raw.parquet', index=False, engine='pyarrow')

# Mostrar estatísticas
print("\n" + "="*60)
print("DADOS BRUTOS GERADOS COM SUCESSO!")
print("="*60)

print("\n📊 GOOGLE ANALYTICS 4 - EVENTOS BRUTOS")
print(f"Total de eventos: {len(df_ga4):,}")
print(f"\nDistribuição de eventos:")
print(df_ga4['event_name'].value_counts())
print(f"\nFontes de tráfego:")
print(df_ga4['traffic_source_source'].value_counts())
print(f"\nDispositivos:")
print(df_ga4['device_category'].value_counts())

print("\n📱 META ADS - DADOS BRUTOS DIÁRIOS")
print(f"Total de linhas: {len(df_meta):,}")
print(f"Período: {df_meta['date'].min()} até {df_meta['date'].max()}")
print(f"\nCampanhas únicas: {df_meta['campaign_id'].nunique()}")
print(f"Ad Sets únicos: {df_meta['ad_set_id'].nunique()}")
print(f"\nPlataformas:")
print(df_meta['platform'].value_counts())

print("\n" + "="*60)
print("Arquivos gerados:")
print("  - ga4_events_raw.parquet (eventos individuais)")
print("  - meta_ads_raw.parquet (dados diários por campanha/adset)")
print("="*60)

# Preview dos dados
print("\n📋 PREVIEW - GA4 Eventos (primeiras 5 linhas):")
print(df_ga4.head())

print("\n📋 PREVIEW - Meta Ads Raw (primeiras 5 linhas):")
print(df_meta.head())