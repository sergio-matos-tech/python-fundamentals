# Sprites 2D com GLFW + OpenGL 3.3 Core

**UFU - FACOM - Computação Gráfica**
**Discente:** Sergio Henrique Ribeiro Matos
**Matrícula:** 12211bcc038

Atividade prática complementar à Atividade 2 (*A Técnica de Sprites na Computação Gráfica 2D: História, Pipeline de GPU e Ferramentas*). O projeto renderiza um personagem animado sobre um cenário em tilemap, usando apenas um Texture Atlas gerado proceduralmente (nenhuma imagem externa é necessária).

## Instalação e execução

Requer Python 3.10+ e uma GPU/driver com suporte a OpenGL 3.3.

```bash
pip install -r requirements.txt
python main.py
```

### Controles

| Tecla | Ação |
|-------|------|
| `A` / `←` | Move para a esquerda e anima |
| `D` / `→` | Move para a direita e anima |
| `Espaço` / `W` / `↑` | Pula |
| `R` | Reinicia a fase |
| `ESC` | Sai da aplicação |

### Objetivo

Coletar as 8 moedas espalhadas pelas plataformas. O contador aparece no título da janela e como ícones de moeda no canto superior esquerdo (HUD desenhado com o mesmo pipeline de sprites).

## Metodologia e Arquitetura do Pipeline 2D

| Requisito teórico | Implementação no código |
|---|---|
| **Quad indexado** | `SpriteRenderer._init_quad_geometry`: 4 vértices (posição + UV) em um VBO e 6 índices em um EBO, encapsulados em um VAO. O desenho usa `glDrawElements`, com dois triângulos compartilhando a diagonal. |
| **Matriz ortográfica** | `SpriteRenderer._create_ortho_matrix(0, 768, 576, 0)` converte coordenadas de mundo em pixels (origem no canto superior esquerdo) para o espaço de recorte. É enviada ao shader como `uProjection`. |
| **Texture Atlas (Sprite Sheet)** | `ProceduralAtlasGenerator` cria com NumPy uma única textura RGBA de 64×32 com células de 16×16. A linha 0 tem 4 quadros do personagem e a linha 1 tem 4 tiles de cenário. |
| **Cálculo de UV no shader** | O Vertex Shader calcula `vTexCoord = texCoord * uUvScale + uUvOffset`, recortando a célula do atlas. `uFlipX` espelha o sprite horizontalmente (equivalente ao flip do OAM). Posição e escala também são aplicadas no shader (`uPosition`, `uScale`). |
| **Nearest Neighbor** | `create_gpu_texture` define `GL_NEAREST` para minificação e magnificação, e `GL_CLAMP_TO_EDGE` para evitar *texture bleeding*. O resultado é pixel-perfect. |
| **Alpha Blending** | `glEnable(GL_BLEND)` com `glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)`. O fragment shader também descarta fragmentos praticamente transparentes. |
| **Delta-Time** | `AnimatedCharacter.update` acumula `dt` em `frame_timer`. Quando o acumulador atinge `frame_duration` (0,12 s), o quadro avança. Assim a animação independe da taxa de quadros. |
| **Tilemap** | `TilemapScene.grid` é uma matriz 9×12 de inteiros. Cada valor indexa um tile da linha 1 do atlas (`-1` = vazio), e o cenário é desenhado com um quad por célula. |
| **Física e colisão (extra)** | `AnimatedCharacter.update` aplica gravidade e pulo integrando a velocidade vertical com `dt`. A colisão é AABB contra o tilemap, resolvida por eixo (X e depois Y): os tiles 0, 1 e 2 são sólidos. A hitbox é menor que o sprite, pois a arte não ocupa toda a célula. |
| **Coleta de moedas (extra)** | `TilemapScene.collect_coins` remove do grid os tiles de moeda (id 3) que intersectam a hitbox. O HUD reutiliza `draw_sprite` com o tile de moeda. |

## Estrutura

```
18-Sprites/
├── main.py            # Código-fonte
├── requirements.txt   # Dependências
└── README.md
```
