# Animação com sprites (GLFW + OpenGL)

Atividade complementar da Atividade 2 (técnica de sprites em computação gráfica 2D).

O personagem é animado a partir de uma sprite sheet (`spritesheet.png`, células de 16x16):

- linha 0: 4 quadros da caminhada
- linha 1: tiles do cenário (grama, terra, nuvem e arbusto)
- linha 2: bloco, bloco usado e moeda

Cada sprite é desenhado recortando a região da textura pelas coordenadas UV.

O personagem pode pular e bater a cabeça nos blocos. Cada bloco rende 1 ponto (uma moeda aparece no canto da tela) e depois fica "usado".

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

Controles: setas ou A/D para andar, espaço/W/seta para cima para pular, R para reiniciar, ESC para sair.

`gerar_spritesheet.py` recria o `spritesheet.png` caso precise. `demo.mp4` mostra a aplicação rodando.
