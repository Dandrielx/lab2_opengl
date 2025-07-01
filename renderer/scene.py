from OpenGL.GL import *
from matrices import (
    rotation_x,
    rotation_y,
    rotation_z,
    translation_matrix,
    perspective_matrix,
    orthographic_matrix,
)
from renderer.tessellation import draw_tessellated_cuboid
from renderer.walls import draw_window_wall
from renderer.furniture import draw_tables, draw_board
from utils.materials import draw_cuboid, draw_elliptical_cylinder


def draw_scene(camera, projection_mode):
    """
    Função principal de renderização. É chamada a cada quadro para desenhar todos os
    elementos da cena 3D.
    :camera: O objeto da câmera que define o ponto de vista.
    :projection_mode: A string que define o tipo de projeção.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa os buffers de cor e de profundidade antes de desenhar um novo quadro.

    # --- PROJEÇÃO ---
    glMatrixMode(GL_PROJECTION) # Define a matriz de Projeção como a matriz ativa.
    glLoadIdentity() # Reseta a matriz de projeção para a matriz identidade.

    if projection_mode == "perspective":
        glLoadMatrixf(perspective_matrix(50, (1280 / 720), 0.1, 100.0).T)
    else:
        glLoadMatrixf(orthographic_matrix(-10, 10, -5, 5, -10, 100).T)

    # --- VISÃO DA CÂMERA ---
    glMatrixMode(GL_MODELVIEW) # Define a matriz de Modelo/Visão como a matriz ativa.
    glLoadIdentity() # Reseta a matriz para a câmera ficar na origem (0,0,0).

    glEnable(GL_LIGHTING) # Ativa o sistema de iluminação do OpenGL.
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.45, 0.45, 0.45, 1.0]) # Define uma luz ambiente global para a cena, garantindo que mesmo as áreas
                                                                    # não iluminadas diretamente não fiquem totalmente pretas.

    # --- LUZES DAS JANELAS ---

    # Configura 3 fontes de luz pontuais para simular a luz vindo das janelas.
    light_color_diffuse = [1.0, 0.98, 0.9, 1.0]
    light_color_specular = [1.0, 1.0, 1.0, 1.0]
    attenuation = 0.004
    window_positions_z = [-7.0, 0.0, 7.0]
    lights = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2]

    for i, light in enumerate(lights):
        glEnable(light)
        glLightfv(light, GL_POSITION, [-10.5, 3.0, window_positions_z[i], 1.0])
        glLightfv(light, GL_DIFFUSE, light_color_diffuse)
        glLightfv(light, GL_SPECULAR, light_color_specular)
        glLightf(light, GL_QUADRATIC_ATTENUATION, attenuation)

    # --- APLICA A CÂMERA ---
    camera.get_view_matrix() # Aplica a matriz de visão da câmera. Isso "move" o mundo inteiro na frente da
                             # câmera, em vez de mover a câmera. É chamado DEPOIS da configuração das luzes
                             # para que as luzes permaneçam fixas no mundo.

    # --- PISO ---
    floor_color = (0.7, 0.7, 0.6, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(3.5, -0.05, 0).T)
    draw_tessellated_cuboid((13, 0.1, 25), floor_color, 32.0, (5, 1, 5))
    glPopMatrix()
    
    # --- PAREDE DO FUNDO ---
    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(3.5, 2.5, -12.5).T)
    draw_cuboid((13, 5, 0.1), wall_color)
    glPopMatrix()

    # --- PAREDE DA DIREITA ---
    glPushMatrix()
    glMultMatrixf(translation_matrix(10, 2.5, 0).T)
    draw_cuboid((0.1, 5, 25), wall_color)
    glPopMatrix()

    # --- TETO ---
    ceiling_color = (0.95, 0.95, 1.0, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(3.5, 5.05, 0).T)
    draw_tessellated_cuboid((13, 0.1, 25), ceiling_color, 10.0, (5, 1, 5))
    glPopMatrix()


    # --- PAREDE DE TRÁS---
    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(2, 2.5, 12.5).T)
    draw_cuboid((10, 5, 0.1), wall_color)
    glPopMatrix()

    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(9.5, 2.5, 12.5).T)
    draw_cuboid((1, 5, 0.1), wall_color)
    glPopMatrix()

    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(8, 4.25, 12.5).T)
    draw_cuboid((2, 1.5, 0.1), wall_color)
    glPopMatrix()

    # --- PORTA ---
    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(8.25, 1.75, 11.8).T)
    glMultMatrixf(rotation_y(45))
    draw_cuboid((2, 3.5, 0.1), wall_color)
    glPopMatrix()

    # --- PAREDE COM AS JANELAS ---
    draw_window_wall()

    # --- MESAS, MONITORES E CADEIRAS ---
    draw_tables()

    # --- QUADRO BRANCO COM LINHA FEITA COM BRESENHAM ---
    draw_board()

    # --- FONTE DO QUADRO ---
    glPushMatrix()
    glMultMatrixf(translation_matrix(3.5, 3.75, -12.3).T)
    draw_cuboid((5.25, 0.25, 0.1), color=(0.05, 0.05, 0.05, 1.0))
    glPopMatrix()

    # --- ARES-CONDICIONADOS ---
    glPushMatrix()
    glMultMatrixf(translation_matrix(-1.5, 4, -12.3).T)
    glMultMatrixf(rotation_z(90))
    draw_elliptical_cylinder(a=0.7/2, b=0.8/2, height=2, color=floor_color)
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(translation_matrix(6.5, 4, -12.3).T)
    glMultMatrixf(rotation_z(90))
    draw_elliptical_cylinder(a=0.7/2, b=0.8/2, height=2, color=floor_color)
    glPopMatrix()
