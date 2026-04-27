# Classe Pai (Superclasse)
class Veiculo:

    # Método construtor da classe pai
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.ligado = False

    def ligar(self):
        self.ligado = True
        print(f"O {self.modelo} foi ligado.")

    def desligar(self):
        self.ligado = False
        print(f"O {self.modelo} foi desligado.")

# Classe Filha (Subclasse) que herda de Veiculo
class Carro(Veiculo):

    # Método construtor da classe filha
    def __init__(self, marca, modelo, portas):
        # super().__init__() chama o construtor da classe pai
        super().__init__(marca, modelo)
        self.portas = portas

    def exibir_info_carro(self):
        print(f"Carro: {self.marca} {self.modelo}, Portas: {self.portas}")

# Outra Classe Filha
class Moto(Veiculo):

    # Método construtor da classe filha
    def __init__(self, marca, modelo, cilindradas):
        super().__init__(marca, modelo)
        self.cilindradas = cilindradas

    # Este método é específico da classe Moto
    def empinar(self):
        print(f"A moto {self.modelo} está empinando! Cuidado!")
        
        
meu_carro = Carro("Volkswagen", "Golf", 4)
minha_moto = Moto("Honda", "CB 500", 500)

meu_carro.exibir_info_carro()
meu_carro.ligar() # Método herdado de Veiculo
minha_moto.ligar() # Método herdado de Veiculo
minha_moto.empinar() # Método específico de Moto

