import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# Configuração global de estilo para os gráficos
sns.set_style("whitegrid")


def dsa_gera_dados_ficticios(num_registros=1000):
    """
    Gera um DataFrame com dados de vendas fictícios, com um catálogo expandido
    e distribuição aleatória ao longo do ano.
    """
    print(f"Iniciando a geração de {num_registros} registros de vendas...\n")

    produtos = {
        # Eletrônicos
        'Laptop Gamer': {'categoria': 'Eletrônicos', 'preco': 7500.00},
        'Monitor Ultrawide 34"': {'categoria': 'Eletrônicos', 'preco': 2800.00},
        'Smartphone Topo de Linha': {'categoria': 'Eletrônicos', 'preco': 5200.00},
        'Tablet Produtividade': {'categoria': 'Eletrônicos', 'preco': 3500.00},
        # Hardware
        'Placa de Vídeo RTX 4070': {'categoria': 'Hardware', 'preco': 4500.00},
        'Processador i9': {'categoria': 'Hardware', 'preco': 3200.00},
        'SSD NVMe 2TB': {'categoria': 'Hardware', 'preco': 850.00},
        'Memória RAM 32GB DDR5': {'categoria': 'Hardware', 'preco': 900.00},
        'Placa Mãe High-End': {'categoria': 'Hardware', 'preco': 1500.00},
        # Acessórios
        'Mouse Vertical Ergonômico': {'categoria': 'Acessórios', 'preco': 250.00},
        'Teclado Mecânico Switch Brown': {'categoria': 'Acessórios', 'preco': 550.00},
        'Headset Wireless 7.1': {'categoria': 'Acessórios', 'preco': 800.00},
        'Webcam 4K': {'categoria': 'Acessórios', 'preco': 700.00},
        'Mousepad Gigante': {'categoria': 'Acessórios', 'preco': 120.00},
        # Móveis
        'Cadeira Gamer Ergonômica': {'categoria': 'Móveis', 'preco': 1600.00},
        'Mesa em L para Escritório': {'categoria': 'Móveis', 'preco': 950.00},
        'Suporte Articulado Monitor': {'categoria': 'Móveis', 'preco': 350.00},
        # Software/Serviços
        'Assinatura Cloud 1TB (Anual)': {'categoria': 'Software', 'preco': 200.00},
        'Licença Suíte Office': {'categoria': 'Software', 'preco': 450.00}
    }

    lista_produtos = list(produtos.keys())
    cidades_estados = {
        'São Paulo': 'SP', 'Rio de Janeiro': 'RJ', 'Belo Horizonte': 'MG',
        'Porto Alegre': 'RS', 'Florianópolis': 'SC', 'Curitiba': 'PR', 
        'Salvador': 'BA', 'Recife': 'PE', 'Fortaleza': 'CE', 'Brasília': 'DF'
    }
    lista_cidades = list(cidades_estados.keys())
    dados_vendas = []
    
    data_inicial = datetime(2026, 1, 1)

    for i in range(num_registros):
        produto_nome = random.choice(lista_produtos)
        cidade = random.choice(lista_cidades)
        # Mais chances de comprar 1 ou 2 itens do que 7
        quantidade = np.random.choice([1, 1, 2, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.05, 0.05, 0.03, 0.02])
        
        # Sorteia um dia aleatório do ano e uma hora aleatória
        dias_adicionais = random.randint(0, 364)
        horas_adicionais = random.randint(0, 23)
        minutos_adicionais = random.randint(0, 59)
        data_pedido = data_inicial + timedelta(days=dias_adicionais, hours=horas_adicionais, minutes=minutos_adicionais)

        # Simula pequenas variações de preço (promoções ou inflação)
        variacao_preco = np.random.uniform(0.95, 1.05) 
        preco_unitario = produtos[produto_nome]['preco'] * variacao_preco

        dados_vendas.append({
            'ID_Pedido': 1000 + i,
            'Data_Pedido': data_pedido,
            'Nome_Produto': produto_nome,
            'Categoria': produtos[produto_nome]['categoria'],
            'Preco_Unitario': round(preco_unitario, 2),
            'Quantidade': quantidade,
            'ID_Cliente': np.random.randint(100, 500), 
            'Cidade': cidade,
            'Estado': cidades_estados[cidade]
        })
    
    print("Geração de dados concluída.")
    return pd.DataFrame(dados_vendas)



def transformar_dados(df):
    """
    Realiza a engenharia de atributos: cria novas colunas necessárias para a análise.
    """
    print("\nIniciando transformação dos dados...")
    
    df['Valor_Total'] = df['Preco_Unitario'] * df['Quantidade']
    
    df['Mes'] = df['Data_Pedido'].dt.month
    df['Ano'] = df['Data_Pedido'].dt.year
    
    print("Transformação concluída. Novas colunas adicionadas: 'Valor_Total', 'Mes', 'Ano'.")
    return df



def plotar_vendas_por_categoria(df):
    """
    Gera um gráfico de barras com o total de vendas por categoria de produto.
    """
    print("\nGerando gráfico de Vendas por Categoria...")
    
    df_categoria = df.groupby('Categoria')['Valor_Total'].sum().reset_index()
    df_categoria = df_categoria.sort_values(by='Valor_Total', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Categoria', y='Valor_Total', data=df_categoria, palette='viridis', hue='Categoria')
    
    plt.title('Receita Total por Categoria de Produto', fontsize=16)
    plt.xlabel('Categoria', fontsize=12)
    plt.ylabel('Receita Total (R$)', fontsize=12)
    
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.tight_layout()
    plt.show()



def plotar_tendencia_mensal(df):
    """
    Gera um gráfico de linha mostrando a evolução do faturamento mês a mês.
    """
    print("\nGerando gráfico de Tendência Mensal...")
    
    df_mensal = df.groupby('Mes')['Valor_Total'].sum().reset_index()
    
    meses_nomes = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    df_mensal['Mes_Nome'] = df_mensal['Mes'].map(meses_nomes)
    
    plt.figure(figsize=(12, 6))
    
    sns.lineplot(x='Mes_Nome', y='Valor_Total', data=df_mensal, marker='o', color='#2ca02c', linewidth=2.5)
    
    plt.title('Tendência de Faturamento Mensal (2026)', fontsize=16)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Faturamento Total (R$)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.tight_layout()
    plt.show()



def plotar_vendas_por_estado(df):
    """
    Gera um gráfico de barras horizontais mostrando o faturamento total por Estado.
    """
    print("\nGerando gráfico de Vendas por Estado...")
    
    df_estado = df.groupby('Estado')['Valor_Total'].sum().reset_index()
    df_estado = df_estado.sort_values(by='Valor_Total', ascending=False)
    
    plt.figure(figsize=(10, 6))
    
    sns.barplot(x='Valor_Total', y='Estado', data=df_estado, palette='magma', hue='Estado')
    
    plt.title('Faturamento Total por Estado (2026)', fontsize=16)
    plt.xlabel('Faturamento Total (R$)', fontsize=12)
    plt.ylabel('Estado', fontsize=12)
    
    plt.ticklabel_format(style='plain', axis='x')
    
    plt.tight_layout()
    plt.show()
    
    

def carregar_dados(df):
    """
    Exporta o DataFrame processado para ficheiros locais (CSV e Parquet).
    Cria um diretório de saída caso não exista.
    """
    print("\nIniciando a etapa de Carga (Load) dos dados...")
    
    pasta_destino = 'dados_exportados'
    
    # Verifica se a pasta existe; se não, cria-a
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Diretório '{pasta_destino}' criado com sucesso.")
        
    # 1. Exportar para CSV
    caminho_csv = os.path.join(pasta_destino, 'vendas_tratadas.csv')
    df.to_csv(caminho_csv, index=False, encoding='utf-8')
    print(f"[+] Dados guardados em formato CSV: {caminho_csv}")
    
    # 2. Exportar para Parquet
    caminho_parquet = os.path.join(pasta_destino, 'vendas_tratadas.parquet')
    df.to_parquet(caminho_parquet, index=False)
    print(f"[+] Dados guardados em formato Parquet: {caminho_parquet}")



if __name__ == '__main__':
    # 1. Extração (Extract)
    df_vendas = dsa_gera_dados_ficticios(4000)
    
    # 2. Transformação (Transform)
    df_vendas = transformar_dados(df_vendas)
    
    # 3. Carga (Load) - Persistência dos Dados
    carregar_dados(df_vendas)
    
    # 4. Visualização / Análise Exploratória
    print("\n--- A gerar visualizações ---")
    plotar_vendas_por_categoria(df_vendas)
    plotar_tendencia_mensal(df_vendas)
    plotar_vendas_por_estado(df_vendas)
    