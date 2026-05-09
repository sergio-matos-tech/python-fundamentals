class Carro:
    
    # O método __init__ é um "construtor". Ele é chamado quando um novo objeto é criado.
    # 'self' se refere à instância do objeto que está sendo criado.
    def __init__(self, marca, modelo, ano):
        
        # Atributos (dados) do objeto
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.ligado = False # Um carro começa desligado por padrão

    # Métodos (comportamentos) do objeto
    def ligar(self):
        
        if not self.ligado:
            self.ligado = True
            print(f"O {self.modelo} está ligado.")
        else:
            print(f"O {self.modelo} já estava ligado.")

    def desligar(self):
        
        if self.ligado:
            self.ligado = False
            print(f"O {self.modelo} foi desligado.")
        else:
            print(f"O {self.modelo} já estava desligado.")

    def exibir_informacoes(self):
        print(f"Marca: {self.marca}, Modelo: {self.modelo}, Ano: {self.ano}")
        
        
carro_1 = Carro("Volkswagen", "Fusca", 1967)
carro_2 = Carro("Tesla", "Model S", 2025)
carro_3 = Carro("Volkswagen", "Fusca", 1967)

print(carro_1.exibir_informacoes())
print(carro_2.exibir_informacoes())
print(carro_1 is carro_3)
print(carro_1 == carro_3)

