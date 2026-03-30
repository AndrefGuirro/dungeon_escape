import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

TITLE = "Fuga da Masmorra"

# Estados do jogo
ESTADO_MENU = "menu"
ESTADO_JOGO = "playing"
ESTADO_VITORIA = "vitoria"

estado_jogo = ESTADO_MENU

som_ativo = True

# Configuração do grid
TAMANHO_TILE = 50
GRID_LARGURA = WIDTH // TAMANHO_TILE
GRID_ALTURA = HEIGHT // TAMANHO_TILE

# Tempo de jogo
tempo_sobrevivencia = 0
tempo_vitoria = 20 * 60  # 20 segundos


class SpriteAnimado:
    def __init__(self, imagens, posicao):
        self.imagens = imagens
        self.indice = 0
        self.temporizador = 0
        self.posicao = posicao

    def atualizar_animacao(self):
        self.temporizador += 1
        if self.temporizador >= 10:
            self.temporizador = 0
            self.indice = (self.indice + 1) % len(self.imagens)

    def desenhar(self):
        screen.blit(self.imagens[self.indice], self.posicao)


class Jogador:
    def __init__(self):
        self.x = 1
        self.y = 1

        self.animacao_parado = ["player_idle_1", "player_idle_2"]
        self.animacao_andando = ["player_walk_1", "player_walk_2"]

        self.sprite = SpriteAnimado(self.animacao_parado, self.obter_posicao())

    def obter_posicao(self):
        return (self.x * TAMANHO_TILE, self.y * TAMANHO_TILE)

    def atualizar(self):
        self.sprite.posicao = self.obter_posicao()
        self.sprite.atualizar_animacao()

    def mover(self, dx, dy):
        novo_x = self.x + dx
        novo_y = self.y + dy

        if 0 <= novo_x < GRID_LARGURA and 0 <= novo_y < GRID_ALTURA:
            self.x = novo_x
            self.y = novo_y
            self.sprite.imagens = self.animacao_andando

    def desenhar(self):
        self.sprite.desenhar()


class Inimigo:
    def __init__(self):
        self.x = random.randint(3, GRID_LARGURA - 1)
        self.y = random.randint(3, GRID_ALTURA - 1)

        self.sprite = SpriteAnimado(
            ["enemy_1", "enemy_2"], self.obter_posicao()
        )

        self.tempo_movimento = 0

    def obter_posicao(self):
        return (self.x * TAMANHO_TILE, self.y * TAMANHO_TILE)

    def atualizar(self):
        self.tempo_movimento += 1

        if self.tempo_movimento > 30:
            self.tempo_movimento = 0
            self.movimento_aleatorio()

        self.sprite.posicao = self.obter_posicao()
        self.sprite.atualizar_animacao()

    def movimento_aleatorio(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        self.x = max(0, min(GRID_LARGURA - 1, self.x + dx))
        self.y = max(0, min(GRID_ALTURA - 1, self.y + dy))

    def desenhar(self):
        self.sprite.desenhar()


jogador = Jogador()
inimigos = [Inimigo() for _ in range(3)]

# Botões
botao_iniciar = Rect((300, 200), (200, 50))
botao_som = Rect((300, 300), (200, 50))
botao_sair = Rect((300, 400), (200, 50))


def desenhar_menu():
    screen.fill((30, 30, 40))

    screen.draw.text("FUGA DA MASMORRA", center=(400, 100), fontsize=50)

    screen.draw.filled_rect(botao_iniciar, (100, 200, 100))
    screen.draw.text("INICIAR", center=botao_iniciar.center)

    screen.draw.filled_rect(botao_som, (200, 200, 100))
    texto = "SOM: ON" if som_ativo else "SOM: OFF"
    screen.draw.text(texto, center=botao_som.center)

    screen.draw.filled_rect(botao_sair, (200, 100, 100))
    screen.draw.text("SAIR", center=botao_sair.center)


def desenhar_jogo():
    screen.fill((0, 0, 0))

    for x in range(GRID_LARGURA):
        for y in range(GRID_ALTURA):
            screen.blit("floor", (x * TAMANHO_TILE, y * TAMANHO_TILE))

    jogador.desenhar()

    for inimigo in inimigos:
        inimigo.desenhar()

    # Mostrar tempo
    screen.draw.text(
        f"Tempo: {tempo_sobrevivencia // 60}",
        (10, 10),
        fontsize=30
    )


def desenhar_vitoria():
    screen.fill((0, 50, 0))

    screen.draw.text("VENCEDOR, sobreviveu 20 segundos!", center=(400, 250), fontsize=60)
    screen.draw.text("Clique para voltar ao menu", center=(400, 350), fontsize=30)


def atualizar_jogo():
    global tempo_sobrevivencia, estado_jogo

    tempo_sobrevivencia += 1

    jogador.atualizar()

    for inimigo in inimigos:
        inimigo.atualizar()

        if inimigo.x == jogador.x and inimigo.y == jogador.y:
            if som_ativo:
                sounds.hit.play()
            reiniciar_jogo()

    # Verificar vitória
    if tempo_sobrevivencia >= tempo_vitoria:
        estado_jogo = ESTADO_VITORIA


def reiniciar_jogo():
    global jogador, inimigos, tempo_sobrevivencia
    jogador = Jogador()
    inimigos = [Inimigo() for _ in range(3)]
    tempo_sobrevivencia = 0


def on_mouse_down(pos):
    global estado_jogo, som_ativo

    if estado_jogo == ESTADO_MENU:
        if botao_iniciar.collidepoint(pos):
            estado_jogo = ESTADO_JOGO
            if som_ativo:
                sounds.click.play()
                music.play("bg_music")

        elif botao_som.collidepoint(pos):
            som_ativo = not som_ativo
            if som_ativo:
                sounds.click.play()
                music.play("bg_music")
            else:
                music.stop()

        elif botao_sair.collidepoint(pos):
            exit()

    elif estado_jogo == ESTADO_VITORIA:
        estado_jogo = ESTADO_MENU
        reiniciar_jogo()


def on_key_down(key):
    if estado_jogo == ESTADO_JOGO:
        if key == keys.UP:
            jogador.mover(0, -1)
        elif key == keys.DOWN:
            jogador.mover(0, 1)
        elif key == keys.LEFT:
            jogador.mover(-1, 0)
        elif key == keys.RIGHT:
            jogador.mover(1, 0)


def draw():
    if estado_jogo == ESTADO_MENU:
        desenhar_menu()
    elif estado_jogo == ESTADO_JOGO:
        desenhar_jogo()
    elif estado_jogo == ESTADO_VITORIA:
        desenhar_vitoria()


def update():
    if estado_jogo == ESTADO_JOGO:
        atualizar_jogo()


pgzrun.go()