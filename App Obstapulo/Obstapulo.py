import pygame
import random

pygame.init()


LARGURA, ALTURA = 840, 680
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Obstapulo")


PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0, 0, 225)


tamanho_jogador = 30
posicao_x_jogador = 50
posicao_y_jogador = ALTURA - tamanho_jogador - 50
velocidade_y_jogador = 0
gravidade = 1
forca_pulo = -15


obstaculos = []  
velocidade_obstaculo = 5
intervalo_criacao_obstaculo = 100
ultimo_tempo_criacao_obstaculo = pygame.time.get_ticks()


espaco_pressionado = False
tempo_no_ar = 0            
tempo_maximo_no_ar = 10000


obstaculos_pulados = 0
aumento_velocidade = 0.5 


fonte = pygame.font.Font(None, 36 )


def criar_obstaculo():
    largura = random.randint(20, 40)  
    altura = random.randint(50, 150)  
    cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    obstaculo = {
        'retangulo': pygame.Rect(LARGURA, ALTURA - altura - 50, largura, altura),
        'cor': cor,
        'velocidade': velocidade_obstaculo + obstaculos_pulados * aumento_velocidade
    }
    return obstaculo


executando = True
relogio = pygame.time.Clock()
tempo_inicial = pygame.time.get_ticks()


obstaculos.append(criar_obstaculo())

while executando:
    relogio.tick(60)
    tempo_atual = pygame.time.get_ticks()

  
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and posicao_y_jogador == ALTURA - tamanho_jogador - 50:
                velocidade_y_jogador = forca_pulo
                espaco_pressionado = True
                tempo_no_ar = tempo_atual
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                espaco_pressionado = False

   
    if espaco_pressionado and (tempo_atual - tempo_no_ar) < tempo_maximo_no_ar:
        velocidade_y_jogador = forca_pulo
    else:
        velocidade_y_jogador += gravidade

    posicao_y_jogador += velocidade_y_jogador
    if posicao_y_jogador >= ALTURA - tamanho_jogador - 50:
        posicao_y_jogador = ALTURA - tamanho_jogador - 50
        velocidade_y_jogador = 0


    for obstaculo in obstaculos:
        obstaculo['retangulo'].x -= obstaculo['velocidade']
        if obstaculo['retangulo'].x + obstaculo['retangulo'].width < 0:
            obstaculos.remove(obstaculo)

            obstaculos.append(criar_obstaculo())

            obstaculos_pulados += 1

    retangulo_jogador = pygame.Rect(posicao_x_jogador, posicao_y_jogador, tamanho_jogador, tamanho_jogador)
    for obstaculo in obstaculos:
        if retangulo_jogador.colliderect(obstaculo['retangulo']):
            executando = False

    janela.fill(AZUL)
    pygame.draw.rect(janela, VERDE, (0, ALTURA - 50, LARGURA, 50))
    pygame.draw.rect(janela, PRETO, (posicao_x_jogador, posicao_y_jogador, tamanho_jogador, tamanho_jogador))  
    for obstaculo in obstaculos:
        pygame.draw.rect(janela, obstaculo['cor'], obstaculo['retangulo'])

    tempo_decorrido = (tempo_atual - tempo_inicial) // 1000
    texto_tempo = fonte.render(f"Tempo: {tempo_decorrido}", True, BRANCO)
    janela.blit(texto_tempo, (10, 10))

    pygame.display.flip()

pygame.quit()               
