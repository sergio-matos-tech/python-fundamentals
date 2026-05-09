import urllib.request
import urllib.error

try:
    site = urllib.request.urlopen('https://youtube.com')
except urllib.error.URLError as e:
    print("ERRO: Não foi possível acessar o site.")
    print(f"Motivo: {e.reason}")
else:
    print("Tudo ok, o site está acessível.")
finally:
    print("Fim da tentativa de acessar o site.")
