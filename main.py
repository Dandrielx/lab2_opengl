import pygame
from pygame.locals import *
from OpenGL.GL import *
from camera import Camera
from renderer.scene import draw_scene

def main():
    """Função principal que inicializa e executa a aplicação."""
    
    # --- INICIALIZAÇÃO DO PYGAME E JANELA DO OPENGL ---
    pygame.init()  # Inicializa os módulos do Pygame.
    display = (1600, 900)  # Define a resolução da janela.
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # Cria a janela com suporte a OpenGL e double buffering.
    pygame.display.set_caption("Simulação de Sala")  # Define o título da janela.
    pygame.mouse.set_visible(False) # Oculta o cursor do mouse.
    pygame.event.set_grab(True) # Impede o mouse de sair da janela.

    # --- CONFIGURAÇÕES INICIAIS DO OPENGL ---
    glEnable(GL_DEPTH_TEST) # Ativa o teste de profundidade (Z-Buffer) para que objetos próximos ocultem os distantes.
    glShadeModel(GL_SMOOTH) # Define o modelo de sombreamento para Gouraud.
    glEnable(GL_NORMALIZE) # Ativa a normalização automática dos vetores normais.
    glClearColor(0.6, 0.8, 1.0, 1.0) # Define a cor de fundo.

    # --- VARIÁVEIS DE CONTROLE ---
    camera = Camera()  # Cria uma instância da classe Camera para controlar a visão.
    clock = pygame.time.Clock()  # Cria um objeto para controlar a taxa de quadros (FPS).
    pygame.mouse.set_pos(display[0] // 2, display[1] // 2) # Centraliza o mouse na tela.
    last_x, last_y = pygame.mouse.get_pos()  # Armazena a posição inicial do mouse.
    projection_mode = 'perspective'  # Define o modo de projeção inicial.
    running = True  # Variável booleana que controla o loop principal.

    # --- LOOP PRINCIPAL ---
    while running:
        
        dt = clock.tick(60) / 1000.0 # Garante que o loop rode a no máximo 60 FPS e calcula o delta time (dt).
        
        # --- PROCESSAMENTO DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # Verifica se o usuário quer fechar a janela ou pressionou a tecla ESC.
                running = False  # Termina o loop.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: # Verifica se a tecla 'P' foi pressionada para alternar o modo de projeção.
                projection_mode = 'perspective' if projection_mode == 'orthographic' else 'orthographic'

        # --- PROCESSAMENTO DO TECLADO ---
        keys = pygame.key.get_pressed() # Obtém o estado das teclas.
        cam_speed = 5.0 * dt  # Calcula a velocidade da câmera baseada no delta time.
        if keys[pygame.K_w]: camera.process_keyboard('FORWARD', cam_speed)
        if keys[pygame.K_s]: camera.process_keyboard('BACKWARD', cam_speed)
        if keys[pygame.K_a]: camera.process_keyboard('LEFT', cam_speed)
        if keys[pygame.K_d]: camera.process_keyboard('RIGHT', cam_speed)

        # --- PROCESSAMENTO DO MOUSE ---
        curr_x, curr_y = pygame.mouse.get_pos()  # Pega a posição atual do mouse.
        x_offset, y_offset = curr_x - last_x, curr_y - last_y # Calcula o deslocamento do mouse desde o último quadro.
        pygame.mouse.set_pos(display[0] // 2, display[1] // 2) # Reposiciona o mouse no centro da tela.
        last_x, last_y = display[0] // 2, display[1] // 2 # Atualiza a última posição conhecida do mouse para o centro.
        camera.process_mouse_movement(x_offset, y_offset) # Processa o deslocamento.

        # --- RENDERIZAÇÃO E ATUALIZAÇÃO DA TELA ---
        draw_scene(camera, projection_mode)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()