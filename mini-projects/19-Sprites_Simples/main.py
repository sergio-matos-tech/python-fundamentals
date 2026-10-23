import os

import glfw
from OpenGL.GL import *
from PIL import Image

LARGURA, ALTURA = 768, 448
CELULA = 16
ESCALA = 4
TAM = CELULA * ESCALA
COLUNAS, LINHAS = 4, 3

CHAO_Y = ALTURA - 2 * TAM
Y_PERSONAGEM = CHAO_Y - TAM
Y_BLOCOS = CHAO_Y - 3 * TAM

VELOCIDADE = 200
GRAVIDADE = 1800
FORCA_PULO = 600
INTERVALO_QUADRO = 0.12

ARBUSTOS = [96, 448, 640]
POSICOES_BLOCOS = [128, 256, 384, 512, 640]


class Personagem:
    def __init__(self):
        self.x = 100.0
        self.y = float(Y_PERSONAGEM)
        self.vel_y = 0.0
        self.no_chao = True
        self.frame = 0
        self.tempo = 0.0
        self.virado_esquerda = False

    def caixa(self):
        # so a parte desenhada do sprite (colunas 5 a 10, a partir da linha 2)
        return (self.x + 5 * ESCALA, self.y + 2 * ESCALA,
                self.x + 11 * ESCALA, self.y + TAM)

    def atualizar(self, dt, direcao, pular):
        if direcao != 0:
            self.x += direcao * VELOCIDADE * dt
            self.x = max(0, min(self.x, LARGURA - TAM))
            self.virado_esquerda = direcao < 0

        if pular and self.no_chao:
            self.vel_y = -FORCA_PULO
            self.no_chao = False

        self.vel_y += GRAVIDADE * dt
        self.y += self.vel_y * dt
        if self.y >= Y_PERSONAGEM:
            self.y = float(Y_PERSONAGEM)
            self.vel_y = 0.0
            self.no_chao = True

        if not self.no_chao:
            self.frame = 1
            self.tempo = 0.0
        elif direcao != 0:
            self.tempo += dt
            if self.tempo >= INTERVALO_QUADRO:
                self.tempo -= INTERVALO_QUADRO
                self.frame = (self.frame + 1) % 4
        else:
            self.frame = 0
            self.tempo = 0.0


class Bloco:
    def __init__(self, x):
        self.x = x
        self.y = Y_BLOCOS
        self.usado = False


class Jogo:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.personagem = Personagem()
        self.blocos = [Bloco(x) for x in POSICOES_BLOCOS]
        self.nuvens = [[80.0, 20.0, 15.0], [380.0, 40.0, 25.0], [620.0, 10.0, 20.0]]
        self.pontos = 0

    def atualizar(self, dt, direcao, pular):
        p = self.personagem
        p.atualizar(dt, direcao, pular)

        for nuvem in self.nuvens:
            nuvem[0] -= nuvem[2] * dt
            if nuvem[0] < -TAM:
                nuvem[0] = LARGURA

        esq, topo, dir_, _ = p.caixa()
        for bloco in self.blocos:
            base = bloco.y + TAM
            bateu = (p.vel_y < 0 and esq < bloco.x + TAM and dir_ > bloco.x
                     and bloco.y < topo < base)
            if bateu:
                p.y = base - 2 * ESCALA
                p.vel_y = 0.0
                if not bloco.usado:
                    bloco.usado = True
                    self.pontos += 1


def carregar_textura(caminho):
    imagem = Image.open(caminho).convert("RGBA")
    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagem.width, imagem.height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, imagem.tobytes())
    return textura


def configurar_opengl(janela):
    largura_fb, altura_fb = glfw.get_framebuffer_size(janela)
    glViewport(0, 0, largura_fb, altura_fb)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, LARGURA, ALTURA, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.45, 0.7, 0.95, 1.0)


def desenhar_sprite(coluna, linha, x, y, espelhar=False, tam=TAM):
    u0, u1 = coluna / COLUNAS, (coluna + 1) / COLUNAS
    v0, v1 = linha / LINHAS, (linha + 1) / LINHAS
    if espelhar:
        u0, u1 = u1, u0

    glBegin(GL_QUADS)
    glTexCoord2f(u0, v0)
    glVertex2f(x, y)
    glTexCoord2f(u1, v0)
    glVertex2f(x + tam, y)
    glTexCoord2f(u1, v1)
    glVertex2f(x + tam, y + tam)
    glTexCoord2f(u0, v1)
    glVertex2f(x, y + tam)
    glEnd()


def desenhar_quadro(jogo):
    glClear(GL_COLOR_BUFFER_BIT)

    for x, y, _ in jogo.nuvens:
        desenhar_sprite(2, 1, x, y)

    for i in range(LARGURA // TAM):
        desenhar_sprite(0, 1, i * TAM, CHAO_Y)
        desenhar_sprite(1, 1, i * TAM, CHAO_Y + TAM)

    for x in ARBUSTOS:
        desenhar_sprite(3, 1, x, CHAO_Y - TAM)

    for bloco in jogo.blocos:
        desenhar_sprite(1 if bloco.usado else 0, 2, bloco.x, bloco.y)

    p = jogo.personagem
    desenhar_sprite(p.frame, 0, p.x, p.y, p.virado_esquerda)

    for i in range(jogo.pontos):
        desenhar_sprite(2, 2, 10 + i * 36, 10, tam=32)


def tecla_pressionada(janela, *teclas):
    return any(glfw.get_key(janela, t) == glfw.PRESS for t in teclas)


def main():
    if not glfw.init():
        return

    janela = glfw.create_window(LARGURA, ALTURA, "Animacao com sprites", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.swap_interval(1)
    configurar_opengl(janela)

    pasta = os.path.dirname(os.path.abspath(__file__))
    carregar_textura(os.path.join(pasta, "spritesheet.png"))

    jogo = Jogo()
    pontos_no_titulo = -1
    ultimo = glfw.get_time()

    while not glfw.window_should_close(janela):
        agora = glfw.get_time()
        dt = min(agora - ultimo, 0.05)
        ultimo = agora

        glfw.poll_events()
        if tecla_pressionada(janela, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(janela, True)
        if tecla_pressionada(janela, glfw.KEY_R):
            jogo.reiniciar()

        direcao = 0
        if tecla_pressionada(janela, glfw.KEY_LEFT, glfw.KEY_A):
            direcao -= 1
        if tecla_pressionada(janela, glfw.KEY_RIGHT, glfw.KEY_D):
            direcao += 1
        pular = tecla_pressionada(janela, glfw.KEY_SPACE, glfw.KEY_W, glfw.KEY_UP)

        jogo.atualizar(dt, direcao, pular)

        if jogo.pontos != pontos_no_titulo:
            pontos_no_titulo = jogo.pontos
            glfw.set_window_title(
                janela, f"Animacao com sprites - Pontos: {jogo.pontos}/{len(jogo.blocos)}")

        desenhar_quadro(jogo)
        glfw.swap_buffers(janela)

    glfw.terminate()


if __name__ == "__main__":
    main()
