import pygame
import random
import math


class Esfera:
    def __init__(self, x, y, vx, vy, raio, cor):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.raio = raio
        self.cor = cor

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def desenha(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)


def dist(e1, e2):
    return math.sqrt((e1.x - e2.x)**2 + (e1.y - e2.y)**2)

def colide_esferas(e1, e2):
    d = dist(e1, e2)

    if d <= e1.raio + e2.raio:
        # Vetor normal
        nx = (e2.x - e1.x) / d
        ny = (e2.y - e1.y) / d

        # Vetor tangencial
        tx = -ny
        ty = nx

        # Projeção das velocidades
        v1n = e1.vx * nx + e1.vy * ny
        v1t = e1.vx * tx + e1.vy * ty

        v2n = e2.vx * nx + e2.vy * ny
        v2t = e2.vx * tx + e2.vy * ty

        # Troca velocidades normais
        v1n_novo = v2n
        v2n_novo = v1n

        # Recalcula novas velocidades (vx, vy)
        e1.vx = v1n_novo * nx + v1t * tx
        e1.vy = v1n_novo * ny + v1t * ty

        e2.vx = v2n_novo * nx + v2t * tx
        e2.vy = v2n_novo * ny + v2t * ty

        # Ajusta posição para evitar sobreposição
        overlap = (e1.raio + e2.raio) - d
        e1.x -= overlap * nx / 2
        e1.y -= overlap * ny / 2
        e2.x += overlap * nx / 2
        e2.y += overlap * ny / 2

def colide_paredes(esf, larg, alt):
    # Colisão com as paredes esquerda/direita
    if esf.x - esf.raio < 0:
        esf.x = esf.raio
        esf.vx *= -1
    elif esf.x + esf.raio > larg:
        esf.x = larg - esf.raio
        esf.vx *= -1

    # Colisão com as paredes superior/inferior
    if esf.y - esf.raio < 0:
        esf.y = esf.raio
        esf.vy *= -1
    elif esf.y + esf.raio > alt:
        esf.y = alt - esf.raio
        esf.vy *= -1


# --- Parâmetros da Simulação ---
N_ESFERAS = 5
RAIO = 15
VEL_MEDIA = 3
JANELA_TAM = (800, 600)
DT = 0.1# Delta t (intervalo de tempo)

# --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)

# --- Inicialização do Pygame ---
pygame.init()
tela = pygame.display.set_mode(JANELA_TAM)
pygame.display.set_caption("Simulação de Colisões de Esferas")
relogio = pygame.time.Clock()

# --- Criação das Esferas ---
esferas = []
for _ in range(N_ESFERAS):
    x = random.randint(RAIO, JANELA_TAM[0] - RAIO)
    y = random.randint(RAIO, JANELA_TAM[1] - RAIO)
    
    # Gera velocidades aleatórias
    angulo = random.uniform(0, 2 * math.pi)
    vx = VEL_MEDIA * math.cos(angulo) * (random.choice([-1, 1]))
    vy = VEL_MEDIA * math.sin(angulo) * (random.choice([-1, 1]))

    cor = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    esferas.append(Esfera(x, y, vx, vy, RAIO, cor))

# --- Loop Principal da Simulação ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 1. Atualizar Posições
    for esf in esferas:
        esf.move(DT)

    # 2. Tratar Colisões com Paredes
    for esf in esferas:
        colide_paredes(esf, JANELA_TAM[0], JANELA_TAM[1])

    # 3. Tratar Colisões entre Esferas
    for i in range(len(esferas)):
        for j in range(i + 1, len(esferas)): # Evita testar a mesma dupla duas vezes e uma esfera consigo mesma
            colide_esferas(esferas[i], esferas[j])

    # 4. Desenhar na Tela
    tela.fill(PRETO)
    for esf in esferas:
        esf.desenha(tela)

    pygame.display.flip()

    # Controla o FPS
    relogio.tick(60)

pygame.quit()