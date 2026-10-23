import sys
import ctypes
import math
from dataclasses import dataclass
from typing import Iterator
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


VERTEX_SHADER_SRC = """
#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 vTexCoord;

uniform mat4 uProjection;
uniform vec2 uPosition;
uniform vec2 uScale;
uniform vec2 uUvOffset;
uniform vec2 uUvScale;
uniform bool uFlipX;

void main() {
    vec2 worldPos = aPos * uScale + uPosition;
    gl_Position = uProjection * vec4(worldPos, 0.0, 1.0);
    
    vec2 texCoord = aTexCoord;
    if (uFlipX) {
        texCoord.x = 1.0 - texCoord.x;
    }
    
    vTexCoord = texCoord * uUvScale + uUvOffset;
}
"""

FRAGMENT_SHADER_SRC = """
#version 330 core
in vec2 vTexCoord;
out vec4 FragColor;

uniform sampler2D uAtlasTexture;

void main() {
    vec4 texColor = texture(uAtlasTexture, vTexCoord);
    if (texColor.a < 0.05) {
        discard;
    }
    FragColor = texColor;
}
"""


class ProceduralAtlasGenerator:
    """
    Gera um Texture Atlas RGBA (64x32 pixels, dividido em células de 16x16)
    diretamente na RAM usando NumPy para garantir execução determinística.
    - Linha 0 (y=0): 4 quadros de animação do personagem (corrida/caminhada).
    - Linha 1 (y=1): 4 blocos de cenário (0: Grama, 1: Tijolo, 2: Plataforma, 3: Moeda).
    """
    CELL_SIZE = 16
    COLS = 4
    ROWS = 2

    @classmethod
    def build_atlas_bytes(cls) -> tuple[np.ndarray, int, int]:
        width = cls.COLS * cls.CELL_SIZE
        height = cls.ROWS * cls.CELL_SIZE
        atlas = np.zeros((height, width, 4), dtype=np.uint8)

        for frame in range(4):
            x0 = frame * cls.CELL_SIZE
            y0 = 0
            
            atlas[y0+2:y0+6, x0+5:x0+11] = [40, 140, 255, 255]
            atlas[y0+3:y0+5, x0+8:x0+11] = [180, 245, 255, 255]
            atlas[y0+6:y0+12, x0+5:x0+11] = [200, 200, 220, 255]
            
            if frame == 1:
                atlas[y0+12:y0+15, x0+4:x0+7] = [220, 60, 60, 255]
                atlas[y0+11:y0+14, x0+9:x0+12] = [220, 60, 60, 255]
            elif frame == 3:
                atlas[y0+11:y0+14, x0+4:x0+7] = [220, 60, 60, 255]
                atlas[y0+12:y0+15, x0+9:x0+12] = [220, 60, 60, 255]
            else:
                atlas[y0+12:y0+16, x0+5:x0+7] = [220, 60, 60, 255]
                atlas[y0+12:y0+16, x0+9:x0+11] = [220, 60, 60, 255]

            arm_y = y0 + 7 + (1 if frame in (1, 2) else 0)
            atlas[arm_y:arm_y+3, x0+3:x0+5] = [255, 190, 90, 255]

        y1 = cls.CELL_SIZE

        x_grass = 0 * cls.CELL_SIZE
        atlas[y1:y1+16, x_grass:x_grass+16] = [120, 72, 40, 255]
        atlas[y1:y1+4, x_grass:x_grass+16] = [50, 180, 70, 255]
        atlas[y1+4:y1+6, x_grass+2:x_grass+14:3] = [40, 140, 55, 255]

        x_brick = 1 * cls.CELL_SIZE
        atlas[y1:y1+16, x_brick:x_brick+16] = [90, 95, 110, 255]
        atlas[y1+7:y1+9, x_brick:x_brick+16] = [50, 52, 60, 255]
        atlas[y1:y1+7, x_brick+7:x_brick+9] = [50, 52, 60, 255]
        atlas[y1+9:y1+16, x_brick+3:x_brick+5] = [50, 52, 60, 255]

        x_plat = 2 * cls.CELL_SIZE
        atlas[y1+2:y1+10, x_plat+1:x_plat+15] = [160, 110, 210, 230]

        x_coin = 3 * cls.CELL_SIZE
        atlas[y1+4:y1+12, x_coin+5:x_coin+11] = [255, 215, 30, 255]
        atlas[y1+6:y1+10, x_coin+7:x_coin+9] = [255, 250, 180, 255]

        return atlas, width, height


class SpriteRenderer:
    """
    Gerencia o VAO, VBO, EBO (Quad de 2 triângulos indexados) e Shader Program.
    """
    def __init__(self, screen_width: int, screen_height: int):
        self.shader = compileProgram(
            compileShader(VERTEX_SHADER_SRC, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER_SRC, GL_FRAGMENT_SHADER)
        )
        self.vao, self.vbo, self.ebo = self._init_quad_geometry()
        self.projection = self._create_ortho_matrix(0, screen_width, screen_height, 0)

        glUseProgram(self.shader)
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "uProjection"),
            1, GL_TRUE, self.projection
        )

    @staticmethod
    def _create_ortho_matrix(left: float, right: float, bottom: float, top: float) -> np.ndarray:
        """Matriz de projeção ortográfica 2D (Seção 3 do artigo)."""
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = 2.0 / (right - left)
        mat[1, 1] = 2.0 / (top - bottom)
        mat[2, 2] = -1.0
        mat[0, 3] = -(right + left) / (right - left)
        mat[1, 3] = -(top + bottom) / (top - bottom)
        return mat

    @staticmethod
    def _init_quad_geometry() -> tuple[int, int, int]:
        """Cria um Quad unitário formado por 4 vértices e 6 índices (2 triângulos)."""
        # Formato: [PosX, PosY, U, V]
        vertices = np.array([
            0.0, 0.0,  0.0, 0.0,  # Superior Esquerdo
            1.0, 0.0,  1.0, 0.0,  # Superior Direito
            1.0, 1.0,  1.0, 1.0,  # Inferior Direito
            0.0, 1.0,  0.0, 1.0   # Inferior Esquerdo
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype=np.uint32)

        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)

        glBindVertexArray(vao)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride = 4 * vertices.itemsize
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(2 * vertices.itemsize))

        glBindVertexArray(0)
        return vao, vbo, ebo

    def draw_sprite(
        self,
        texture_id: int,
        position: tuple[float, float],
        scale: tuple[float, float],
        atlas_col: int,
        atlas_row: int,
        total_cols: int = 4,
        total_rows: int = 2,
        flip_x: bool = False
    ) -> None:
        glUseProgram(self.shader)

        uv_scale = (1.0 / total_cols, 1.0 / total_rows)
        uv_offset = (atlas_col * uv_scale[0], atlas_row * uv_scale[1])

        glUniform2f(glGetUniformLocation(self.shader, "uPosition"), *position)
        glUniform2f(glGetUniformLocation(self.shader, "uScale"), *scale)
        glUniform2f(glGetUniformLocation(self.shader, "uUvOffset"), *uv_offset)
        glUniform2f(glGetUniformLocation(self.shader, "uUvScale"), *uv_scale)
        glUniform1i(glGetUniformLocation(self.shader, "uFlipX"), int(flip_x))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def cleanup(self) -> None:
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        glDeleteBuffers(1, [self.ebo])
        glDeleteProgram(self.shader)


Rect = tuple[float, float, float, float]  # (esquerda, topo, direita, base)


class TilemapScene:
    """
    Cenário composto por uma matriz 2D de inteiros onde cada índice aponta
    para um tile no Texture Atlas (-1 = vazio, 0 = grama, 1 = tijolo, 2 = plataforma, 3 = moeda).
    Os tiles 0, 1 e 2 são sólidos (colidem com o personagem); o tile 3 é coletável.
    """
    TILE_SIZE = 64
    SOLID_TILES = frozenset({0, 1, 2})
    COIN_TILE = 3

    # Matriz 9 linhas x 12 colunas (768x576 pixels)
    LAYOUT = (
        (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
        (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
        (-1, -1, -1, -1, -1,  3,  3, -1, -1, -1, -1, -1),
        (-1, -1, -1, -1,  2,  2,  2,  2, -1, -1, -1, -1),
        (-1, -1,  3,  3, -1, -1, -1, -1,  3,  3, -1, -1),
        (-1,  2,  2,  2,  2, -1, -1,  2,  2,  2,  2, -1),
        (-1,  3, -1, -1, -1, -1, -1, -1, -1, -1,  3, -1),
        ( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0),
        ( 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1),
    )

    def __init__(self):
        self.grid: list[list[int]] = []
        self.total_coins = 0
        self.reset()

    def reset(self) -> None:
        """Restaura o cenário original (moedas incluídas)."""
        self.grid = [list(row) for row in self.LAYOUT]
        self.total_coins = sum(row.count(self.COIN_TILE) for row in self.grid)

    def _tiles_in_rect(self, rect: Rect) -> Iterator[tuple[int, int]]:
        """Itera sobre as células (coluna, linha) do grid que o retângulo intersecta."""
        left, top, right, bottom = rect
        ts = self.TILE_SIZE
        for row in range(math.floor(top / ts), math.ceil(bottom / ts)):
            for col in range(math.floor(left / ts), math.ceil(right / ts)):
                yield col, row

    def _tile_at(self, col: int, row: int) -> int:
        """Retorna o id do tile; abaixo do grid é considerado sólido, nas demais bordas vazio."""
        if row >= len(self.grid):
            return 0
        if row < 0 or col < 0 or col >= len(self.grid[row]):
            return -1
        return self.grid[row][col]

    def solid_tiles_in_rect(self, rect: Rect) -> list[tuple[int, int]]:
        return [
            (col, row) for col, row in self._tiles_in_rect(rect)
            if self._tile_at(col, row) in self.SOLID_TILES
        ]

    def collect_coins(self, rect: Rect) -> int:
        """Remove as moedas que intersectam o retângulo e retorna quantas foram coletadas."""
        collected = 0
        for col, row in self._tiles_in_rect(rect):
            if self._tile_at(col, row) == self.COIN_TILE:
                self.grid[row][col] = -1
                collected += 1
        return collected

    def render(self, renderer: SpriteRenderer, texture_id: int) -> None:
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile_id in enumerate(row):
                if tile_id >= 0:
                    pos = (col_idx * self.TILE_SIZE, row_idx * self.TILE_SIZE)
                    scale = (self.TILE_SIZE, self.TILE_SIZE)
                    renderer.draw_sprite(
                        texture_id=texture_id,
                        position=pos,
                        scale=scale,
                        atlas_col=tile_id,
                        atlas_row=1
                    )


@dataclass
class AnimatedCharacter:
    """
    Personagem com animação quadro a quadro (acumulador de delta-time),
    gravidade, pulo e colisão AABB contra o Tilemap.
    """
    x: float
    y: float
    size: float = 64.0
    speed: float = 220.0
    current_frame: int = 0
    frame_timer: float = 0.0
    frame_duration: float = 0.12
    facing_left: bool = False
    vel_y: float = 0.0
    on_ground: bool = False

    # Física (pixels e segundos): altura do pulo = JUMP_SPEED² / (2 * GRAVITY) ≈ 185 px
    GRAVITY = 2000.0
    JUMP_SPEED = 860.0
    MAX_FALL_SPEED = 1000.0

    # Hitbox como fração do sprite (a arte não ocupa toda a célula 16x16)
    HITBOX_LEFT = 0.25
    HITBOX_TOP = 0.125
    HITBOX_RIGHT = 0.75
    HITBOX_BOTTOM = 1.0

    def hitbox(self) -> Rect:
        return (
            self.x + self.size * self.HITBOX_LEFT,
            self.y + self.size * self.HITBOX_TOP,
            self.x + self.size * self.HITBOX_RIGHT,
            self.y + self.size * self.HITBOX_BOTTOM,
        )

    def update(
        self, dt: float, move_dir: float, jump: bool,
        scene: TilemapScene, screen_width: int
    ) -> None:
        ts = scene.TILE_SIZE

        if move_dir != 0.0:
            self.x += move_dir * self.speed * dt
            self.x = max(-self.size * self.HITBOX_LEFT,
                         min(self.x, screen_width - self.size * self.HITBOX_RIGHT))
            self.facing_left = move_dir < 0.0

            for col, _ in scene.solid_tiles_in_rect(self.hitbox()):
                if move_dir > 0.0:
                    self.x = col * ts - self.size * self.HITBOX_RIGHT
                else:
                    self.x = (col + 1) * ts - self.size * self.HITBOX_LEFT

        if jump and self.on_ground:
            self.vel_y = -self.JUMP_SPEED
        self.vel_y = min(self.vel_y + self.GRAVITY * dt, self.MAX_FALL_SPEED)
        self.y += self.vel_y * dt

        falling = self.vel_y > 0.0
        self.on_ground = False
        for _, row in scene.solid_tiles_in_rect(self.hitbox()):
            if falling:
                self.y = row * ts - self.size * self.HITBOX_BOTTOM
                self.on_ground = True
            else:
                self.y = (row + 1) * ts - self.size * self.HITBOX_TOP
            self.vel_y = 0.0

        if not self.on_ground:
            self.current_frame = 1
            self.frame_timer = 0.0
        elif move_dir != 0.0:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration
                self.current_frame = (self.current_frame + 1) % 4
        else:
            self.current_frame = 0
            self.frame_timer = 0.0


WINDOW_TITLE = "UFU - Computacao Grafica | Pipeline 2D: Sprites & Tilemap (Sergio Matos)"


def create_gpu_texture(atlas_data: np.ndarray, width: int, height: int) -> int:
    """Aloca a textura na VRAM configurando Nearest Neighbor (Pixel Art)."""
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, atlas_data
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id


def is_pressed(window, *keys: int) -> bool:
    return any(glfw.get_key(window, key) == glfw.PRESS for key in keys)


def spawn_player() -> AnimatedCharacter:
    """Posiciona o personagem no chão (linha 6 -> y = 6 * 64, logo acima da grama)."""
    return AnimatedCharacter(x=352.0, y=6 * TilemapScene.TILE_SIZE)


def main() -> None:
    if not glfw.init():
        sys.exit("Falha ao inicializar o GLFW.")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

    SCREEN_W, SCREEN_H = 768, 576
    window = glfw.create_window(SCREEN_W, SCREEN_H, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit("Falha ao criar a janela OpenGL.")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    renderer: SpriteRenderer | None = None
    atlas_tex_id = 0

    try:
        # Inicialização de Recursos (dentro do try para garantir a liberação em caso de falha)
        atlas_bytes, atlas_w, atlas_h = ProceduralAtlasGenerator.build_atlas_bytes()
        atlas_tex_id = create_gpu_texture(atlas_bytes, atlas_w, atlas_h)
        renderer = SpriteRenderer(SCREEN_W, SCREEN_H)
        scene = TilemapScene()
        player = spawn_player()
        coins = 0
        shown_coins = -1  # força a atualização inicial do título

        last_time = glfw.get_time()

        while not glfw.window_should_close(window):
            current_time = glfw.get_time()
            # Limita o dt para evitar atravessar tiles após travamentos (ex.: arrastar a janela)
            dt = min(current_time - last_time, 0.05)
            last_time = current_time

            glfw.poll_events()

            if is_pressed(window, glfw.KEY_ESCAPE):
                glfw.set_window_should_close(window, True)

            if is_pressed(window, glfw.KEY_R):
                scene.reset()
                player = spawn_player()
                coins = 0

            move_dir = 0.0
            if is_pressed(window, glfw.KEY_LEFT, glfw.KEY_A):
                move_dir -= 1.0
            if is_pressed(window, glfw.KEY_RIGHT, glfw.KEY_D):
                move_dir += 1.0
            jump = is_pressed(window, glfw.KEY_SPACE, glfw.KEY_W, glfw.KEY_UP)

            player.update(dt, move_dir, jump, scene, SCREEN_W)
            coins += scene.collect_coins(player.hitbox())

            if coins != shown_coins:
                shown_coins = coins
                status = "TODAS COLETADAS! (R reinicia)" if coins == scene.total_coins else ""
                glfw.set_window_title(
                    window, f"{WINDOW_TITLE} | Moedas: {coins}/{scene.total_coins} {status}"
                )

            glClearColor(0.11, 0.14, 0.22, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            scene.render(renderer, atlas_tex_id)

            renderer.draw_sprite(
                texture_id=atlas_tex_id,
                position=(player.x, player.y),
                scale=(player.size, player.size),
                atlas_col=player.current_frame,
                atlas_row=0,
                flip_x=player.facing_left
            )

            for i in range(coins):
                renderer.draw_sprite(
                    texture_id=atlas_tex_id,
                    position=(8 + i * 36, 8),
                    scale=(32, 32),
                    atlas_col=int(TilemapScene.COIN_TILE),
                    atlas_row=1
                )

            glfw.swap_buffers(window)
    finally:
        if renderer is not None:
            renderer.cleanup()
        if atlas_tex_id:
            glDeleteTextures([atlas_tex_id])
        glfw.terminate()


if __name__ == "__main__":
    main()
