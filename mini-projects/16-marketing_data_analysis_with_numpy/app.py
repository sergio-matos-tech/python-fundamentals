import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# np.random.seed(42)

num_usuarios = 5000
visitas = np.random.randint(1, 51, size = num_usuarios)

tempo_no_site = np.random.normal(loc = 20, scale = 5, size = num_usuarios) + (visitas * 0.5)
tempo_no_site = np.round(tempo_no_site, 2) # Arredondar para 2 casas decimais

itens_no_carrinho = np.random.randint(0, 8, size = num_usuarios) + (visitas // 10)
itens_no_carrinho = (itens_no_carrinho + (tempo_no_site // 15)).astype(int)

valor_compra = (itens_no_carrinho * 35) + np.random.normal(loc = 0, scale = 10, size = num_usuarios)

valor_compra[itens_no_carrinho == 0] = 0
valor_compra[valor_compra < 0] = 0 # Corrigir valores negativos que possam surgir
valor_compra = np.round(valor_compra, 2)

dados_ecommerce = np.column_stack((visitas, tempo_no_site, itens_no_carrinho, valor_compra))

df = pd.DataFrame(
    dados_ecommerce,
    columns=["Visitas", "Tempo (min)", "Itens Carrinho", "Valor Compra (R$)"]
)

print("\nShape da nossa massa de dados:", df.shape)
print("\nPrimeiros usuários:\n")
print(df.head(10))

visitas_col = dados_ecommerce[:, 0]
tempo_col   = dados_ecommerce[:, 1]
itens_col   = dados_ecommerce[:, 2]
valor_col   = dados_ecommerce[:, 3]

media_visitas = np.mean(visitas_col)
media_tempo   = np.mean(tempo_col)
media_itens   = np.mean(itens_col)
media_valor = float(np.mean(valor_col))

print('\n--- ANÁLISE ESTATÍSTICA GERAL ---\n')
print(f"\nMédia de Visitas: {media_visitas:.2f}")
print(f"Média de Tempo no Site: {media_tempo:.2f} min")
print(f"Média de Itens no Carrinho: {media_itens:.2f}")
print(f"Média de Valor de Compra (Ticket Médio): R$ {media_valor:.2f}")

mediana_valor = float(np.median(valor_col))
print(f"\nMediana do Valor de Compra: R$ {mediana_valor:.2f}")

std_valor = float(np.std(valor_col))
print(f"Desvio Padrão do Valor de Compra: R$ {std_valor:.2f}")

max_valor = np.max(valor_col)
min_valor_positivo = np.min(valor_col[valor_col > 0]) # Mínimo apenas entre quem comprou
print(f"Maior Valor de Compra: R$ {max_valor:.2f}")
print(f"Menor Valor de Compra (de quem comprou): R$ {min_valor_positivo:.2f}\n")

plt.figure(figsize = (12, 5))
plt.hist(valor_col, bins = 30, color = 'skyblue', edgecolor = 'black', alpha = 0.7)
plt.axvline(media_valor, color = 'red', linestyle = '--', linewidth = 2, label = f'Média = R$ {media_valor:.2f}')
plt.axvline(mediana_valor, color = 'orange', linestyle = '--', linewidth = 2, label = f'Mediana = R$ {mediana_valor:.2f}')
plt.axvline(media_valor + std_valor, color = 'green', linestyle = ':', linewidth = 2, label = f'+1 DP = R$ {media_valor + std_valor:.2f}')
plt.axvline(media_valor - std_valor, color = 'green', linestyle = ':', linewidth = 2, label = f'-1 DP = R$ {media_valor - std_valor:.2f}')
plt.title('Distribuição dos Valores de Compra')
plt.xlabel('Valor da Compra (R$)')
plt.ylabel('Frequência')
plt.legend()
plt.grid(alpha = 0.3)
plt.show()



'''
Quais são as características e comportamentos distintos dos nossos clientes de "Alto Valor"? Eles visitam mais o site? Passam mais tempo navegando?'''


# Filtro booleano para clientes com compras > R$ 250
clientes_alto_valor = dados_ecommerce[dados_ecommerce[:, 3] > 250]

print("\n--- ANÁLISE: CLIENTES DE ALTO VALOR (Compras > R$ 250) ---\n")
print(f"Número de clientes de alto valor: {clientes_alto_valor.shape[0]}")

# Estatísticas deste segmento
media_visitas_alto_valor = float(np.mean(clientes_alto_valor[:, 0]))
media_tempo_alto_valor = float(np.mean(clientes_alto_valor[:, 1]))

print(f"Média de visitas desses clientes: {media_visitas_alto_valor:.2f}")
print(f"Média de tempo no site desses clientes: {media_tempo_alto_valor:.2f} min")


plt.figure()

plt.hist(clientes_alto_valor[:, 3], bins=20)
plt.title("Distribuição de Compras (> R$ 250)")
plt.xlabel("Valor da Compra (R$)")
plt.ylabel("Quantidade de Clientes")

plt.show()



plt.figure()

plt.scatter(
    clientes_alto_valor[:, 0],  # visitas
    clientes_alto_valor[:, 1]   # tempo no site
)

plt.title("Clientes de Alto Valor: Visitas vs Tempo no Site")
plt.xlabel("Número de Visitas")
plt.ylabel("Tempo no Site (min)")

plt.show()

plt.figure()

plt.scatter(
    clientes_alto_valor[:, 0],
    clientes_alto_valor[:, 1]
)

# Médias
plt.axvline(media_visitas_alto_valor)
plt.axhline(media_tempo_alto_valor)

plt.title("Clientes de Alto Valor com Médias")
plt.xlabel("Número de Visitas")
plt.ylabel("Tempo no Site (min)")

plt.show()


plt.figure()

# Todos os usuários
plt.scatter(dados_ecommerce[:, 0], dados_ecommerce[:, 1])

# Destaque alto valor
plt.scatter(
    clientes_alto_valor[:, 0],
    clientes_alto_valor[:, 1]
)

plt.title("Comparação: Todos vs Alto Valor")
plt.xlabel("Visitas")
plt.ylabel("Tempo no Site (min)")

plt.show()



'''
Qual é o comportamento dos usuários que visitam o site, mas não realizam nenhuma compra? Onde está a oportunidade de conversão com este grupo?
'''

# Filtro para visitantes que não compraram
visitantes_sem_compra = dados_ecommerce[dados_ecommerce[:, 3] == 0]

print("\n--- ANÁLISE: VISITANTES QUE NÃO COMPRAM ---\n")
print(f"Número de visitantes que não compraram: {visitantes_sem_compra.shape[0]}")

# Estatísticas deste segmento
media_tempo_sem_compra = float(np.mean(visitantes_sem_compra[:, 1]))
media_visitas_sem_compra = float(np.mean(visitantes_sem_compra[:, 0]))

print(f"Média de visitas desses visitantes: {media_visitas_sem_compra:.2f}")
print(f"Apesar de não comprarem, eles passam em média {media_tempo_sem_compra:.2f} min no site.")

plt.figure()

plt.scatter(
    visitantes_sem_compra[:, 0],  # visitas
    visitantes_sem_compra[:, 1]   # tempo
)

plt.title("Visitantes sem compra: Visitas vs Tempo no Site")
plt.xlabel("Número de Visitas")
plt.ylabel("Tempo no Site (min)")

plt.show()

compradores = dados_ecommerce[dados_ecommerce[:, 3] > 0]

plt.figure()

# Não compradores
plt.scatter(
    visitantes_sem_compra[:, 0],
    visitantes_sem_compra[:, 1],
    label="Não compraram"
)

# Compradores
plt.scatter(
    compradores[:, 0],
    compradores[:, 1],
    label="Compraram"
)

plt.title("Comparação: Compradores vs Não Compradores")
plt.xlabel("Visitas")
plt.ylabel("Tempo no Site (min)")
plt.legend()

plt.show()

alto_potencial = visitantes_sem_compra[
    (visitantes_sem_compra[:, 1] > media_tempo_sem_compra) &
    (visitantes_sem_compra[:, 0] > media_visitas_sem_compra)
]

plt.figure()

# Todos não compradores
plt.scatter(
    visitantes_sem_compra[:, 0],
    visitantes_sem_compra[:, 1],
    label="Não compraram"
)

# Destaque alto potencial
plt.scatter(
    alto_potencial[:, 0],
    alto_potencial[:, 1],
    label="Alto potencial"
)

plt.title("Oportunidade de Conversão")
plt.xlabel("Visitas")
plt.ylabel("Tempo no Site (min)")
plt.legend()

plt.show()

plt.figure()

plt.scatter(
    visitantes_sem_compra[:, 0],
    visitantes_sem_compra[:, 1]
)

plt.axvline(media_visitas_sem_compra)
plt.axhline(media_tempo_sem_compra)

plt.title("Visitantes sem compra com médias")
plt.xlabel("Visitas")
plt.ylabel("Tempo no Site (min)")

plt.show()

'''
### Pergunta 4

Existe uma correlação estatisticamente relevante entre o tempo gasto no site, o número de itens no carrinho e o valor final da compra?
'''


# A função np.corrcoef calcula a matriz de correlação
# rowvar=False indica que as colunas são as variáveis
matriz_correlacao = np.corrcoef(dados_ecommerce, rowvar = False)

print("\n--- MATRIZ DE CORRELAÇÃO ---\n")
print("[Visitas, Tempo, Itens, Valor]\n")
print(np.round(matriz_correlacao, 2))

# Calcula a matriz de correlação
matriz_correlacao = np.corrcoef(dados_ecommerce, rowvar = False)

# Define os nomes das variáveis
nomes_variaveis = ["Visitas", "Tempo no Site", "Itens no Carrinho", "Valor da Compra"]

# Converte em DataFrame para exibir com rótulos
df_correlacao = pd.DataFrame(matriz_correlacao, 
                             index = nomes_variaveis, 
                             columns = nomes_variaveis)

# Matriz de correlação (mapa de calor)
plt.figure(figsize = (7, 5))
sns.heatmap(df_correlacao, annot = True, cmap = "Blues", fmt = ".2f")
plt.title("Matriz de Correlação")
plt.show()


