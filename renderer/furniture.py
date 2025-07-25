from OpenGL.GL import *
from matrices import translation_matrix, rotation_x, rotation_y, rotation_z
from renderer.tessellation import draw_tessellated_cuboid
from utils.materials import draw_cuboid, draw_elliptical_cylinder, set_material, draw_tampo
from utils.raster import bresenham_line
import numpy as np

def draw_tables():

    # --- DEFINIÇÃO DE CORES ---
    table_color = (1, 0.35, 0.35, 1.0)
    leg_color = (0.5, 0.45, 0.35, 1.0)
    lights_color = (0.75, 0.75, 0.75, 1.0)
    support_color = (0.05, 0.05, 0.05, 1.0)

    for row in range(-8, 10, 4): # Loop principal para iterar sobre as fileiras da sala (no eixo Z).

        # --- BLOCO DA PRIMEIRA MESA (MESA MAIOR) ---
                                      
        glPushMatrix() # Isola as transformações para este bloco de mesa.
        glMultMatrixf(translation_matrix(6.9, 1, row).T) # Define a posição base para todo o conjunto da mesa grande.

        # --- TAMPO DA MESA ---
        glPushMatrix()
        final_mat = np.dot(translation_matrix(0, 0.18, 0), rotation_y(180))
        glMultMatrixf(final_mat.T)
        set_material([c*0.4 for c in table_color[:3]], table_color, [1,1,1,1], 128.0)
        draw_tampo(width=6.1, height=0.065, depth=1.2, corner_radius=0.3, segments=15)
        glPopMatrix()
        
        # --- SUPORTE DO TECLADO ---
        glPushMatrix()
        glMultMatrixf(rotation_y(180).T)
        final_mat = np.dot(translation_matrix(0, -0.2, -0.5), rotation_y(180))
        glMultMatrixf(final_mat.T)
        
        set_material([c*0.4 for c in table_color[:3]], table_color, [1,1,1,1], 128.0)
        draw_tampo(width=6.1, height=0.065, depth=1.2, corner_radius=0.3, segments=15)
        glPopMatrix()


        # --- LUZ TETO ---
        for pos in np.arange(-3.7, 3.7+0.1, 3.7):
            glPushMatrix()
            glMultMatrixf(translation_matrix(pos-3.7, 3.95, 0).T)
            draw_cuboid((2.5, 0.2, 0.5), lights_color, shininess=128.0)
            glPopMatrix()

        # --- PERNA DA MESA ---
        for pos in np.arange(-3, 3+0.1, 2):
            glPushMatrix()
            glMultMatrixf(translation_matrix(pos, -0.6, 0.15).T)
            draw_cuboid((0.08, 0.8, 1), leg_color)
            glPopMatrix()

            glPushMatrix()
            glMultMatrixf(translation_matrix(pos, -0.04, -0.2).T)
            draw_cuboid((0.08, 0.38, 0.3), leg_color)
            glPopMatrix()

            if pos < 3:
                draw_chair(pos + 1, -1, 1.2)

        # --- PROTEÇÃO TRASEIRA DA MESA ---
        glPushMatrix()
        final_mat = np.dot(translation_matrix(0, -0.1, -0.35), rotation_y(90))
        glMultMatrixf(final_mat.T)
        draw_cuboid((0.06, 0.5, 6.08), leg_color)
        glPopMatrix()

        # --- MONITOR 1 ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(-1.95, 0.7, 0.3).T)
        draw_cuboid((1, 0.6, 0.05), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, 0, -0.08).T)
        draw_cuboid((0.5, 0.3, 0.15), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.08, -0.12).T)
        draw_cuboid((0.2, 0.8, 0.1), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.4, 0.1).T)
        draw_cuboid((0.8, 0.02, 0.5), support_color, 128)
        glPopMatrix()

        # --- MONITOR 2 ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(1.95, 0.7, 0.3).T)
        draw_cuboid((1, 0.6, 0.05), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, 0, -0.08).T)
        draw_cuboid((0.5, 0.3, 0.15), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.08, -0.12).T)
        draw_cuboid((0.2, 0.8, 0.1), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.4, 0.1).T)
        draw_cuboid((0.8, 0.02, 0.5), support_color, 128)
        glPopMatrix()


        # --- PC 1 ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(-1.95, -0.05 , 0.5).T)
        draw_cuboid((1, 0.3, 0.7), support_color, 128)
        glPopMatrix()

        
        # --- PC 2 ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(1.95, -0.05 , 0.5).T)
        draw_cuboid((1, 0.3, 0.7), support_color, 128)
        glPopMatrix()

        glPopMatrix()



        # --- BLOCO DA SEGUNDA MESA (MESA MENOR) ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(2, 1, row).T)

        # --- TAMPO DA MESA ---
        glPushMatrix()
        final_mat = np.dot(translation_matrix(-0.25, 0.18, 0), rotation_y(180))
        glMultMatrixf(final_mat.T)
        set_material([c*0.4 for c in table_color[:3]], table_color, [1,1,1,1], 128.0)
        draw_tampo(width=4.1, height=0.065, depth=1.2, corner_radius=0.3, segments=15)
        glPopMatrix()
        
        # --- SUPORTE DO TECLADO ---
        glPushMatrix()
        glMultMatrixf(rotation_y(180).T)
        final_mat = np.dot(translation_matrix(0.25, -0.2, -0.5), rotation_y(180))
        glMultMatrixf(final_mat.T)
        
        set_material([c*0.4 for c in table_color[:3]], table_color, [1,1,1,1], 128.0)
        draw_tampo(width=4.1, height=0.065, depth=1.2, corner_radius=0.3, segments=15)
        glPopMatrix()


        # --- PERNAS DA MESA ---
        for pos in np.arange(-2.05, 2.05+0.1, 2.05):
            if pos == 2.05:
                glPushMatrix()
                glMultMatrixf(translation_matrix(pos-0.3, -0.6, 0.15).T)
                draw_cuboid((0.08, 0.8, 1), leg_color)
                glPopMatrix()

                glPushMatrix()
                glMultMatrixf(translation_matrix(pos-0.3, -0.04, -0.2).T)
                draw_cuboid((0.08, 0.38, 0.3), leg_color)
                glPopMatrix()
            else:
                glPushMatrix()
                glMultMatrixf(translation_matrix(pos-0.2, -0.6, 0.15).T)
                draw_cuboid((0.08, 0.8, 1), leg_color)
                glPopMatrix()

                glPushMatrix()
                glMultMatrixf(translation_matrix(pos-0.2, -0.04, -0.2).T)
                draw_cuboid((0.08, 0.38, 0.3), leg_color)
                glPopMatrix()

                draw_chair(pos + 0.8, -1, 1.2)

        # --- PROTEÇÃO TRASEIRA DA MESA ---
        glPushMatrix()
        final_mat = np.dot(translation_matrix(-0.25, -0.1, -0.35), rotation_y(90))
        glMultMatrixf(final_mat.T)
        draw_cuboid((0.06, 0.5, 4.05), leg_color)
        glPopMatrix()

        # --- MONITOR ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(-1.2, 0.7, 0.3).T)
        draw_cuboid((1, 0.6, 0.05), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, 0, -0.08).T)
        draw_cuboid((0.5, 0.3, 0.15), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.08, -0.12).T)
        draw_cuboid((0.2, 0.8, 0.1), support_color, 128)
            
        glMultMatrixf(translation_matrix(0, -0.4, 0.1).T)
        draw_cuboid((0.8, 0.02, 0.5), support_color, 128)
        glPopMatrix()

        # --- PC ---
        glPushMatrix()
        glMultMatrixf(translation_matrix(-1.2, -0.05 , 0.5).T)
        draw_cuboid((1, 0.3, 0.7), support_color, 128)
        glPopMatrix()

        glPopMatrix()
        

def draw_board():
    """Desenha o quadro branco e a linha com o algoritmo de Bresenham sobre ele."""
    glPushMatrix()
    glMultMatrixf(translation_matrix(3.5, 2, -12.4).T)
    draw_cuboid((5, 3.5, 0.1), (1, 1, 1, 1), 10) # Desenha a base retangular branca do quadro.

    glDisable(GL_LIGHTING) # Desabilita temporariamente a iluminação para desenhar a linha com cor pura.
    glColor3f(0.1, 0.1, 0.1) # Define a cor da linha (preto).
    glPointSize(3.0) # Define o tamanho dos pontos da linha.
    glBegin(GL_POINTS)

    # Itera sobre os pontos gerados pelo algoritmo de Bresenham.
    for p in bresenham_line(0, 0, 100, 80): 

        # Mapeia as coordenadas 2D do algoritmo para o espaço 3D do quadro.
        px = -1.9 + (p[0] / 100.0) * 3.8
        py = -0.9 + (p[1] / 80.0) * 1.8
        glVertex3f(px, py, 0.06) # Desenha o ponto ligeiramente à frente do quadro.

    glEnd()
    glEnable(GL_LIGHTING) # Reabilita a iluminação para o resto da cena.
    glPopMatrix()

def draw_chair(pos_x = 0, pos_y = 0, pos_z = 0):
    """
    Desenha uma cadeira completa, parte por parte, usando cilindros elípticos.
    Os parâmetros pos_x, pos_y, pos_z permitem um deslocamento opcional da cadeira.
    """
    seat_color = (0.1, 0.1, 0.1, 1.0)
    support_color = (0 , 0, 0, 1.0)

    # --- ASSENTO DA CADEIRA ---
    glPushMatrix()
    glMultMatrixf(translation_matrix(0 + pos_x, 0.5 + pos_y, 0 + pos_z).T)
    draw_elliptical_cylinder(a=0.7/2, b=0.8/2, height=0.1, color=seat_color)
    glPopMatrix()

    # --- ENCOSTO ---
    # É transladado para trás/cima e rotacionado para ficar vertical.
    glPushMatrix()
    glMultMatrixf(translation_matrix(0 + pos_x, 1.1 + pos_y, 0.3 + pos_z).T)
    glMultMatrixf(rotation_x(90))
    draw_elliptical_cylinder(a=0.6/2, b=0.7/2, height=0.08, color=seat_color)
    glPopMatrix()


    # --- SUPORTES ENCOSTO ---
    for x in [-0.2, 0.2]:
        glPushMatrix()
        glMultMatrixf(translation_matrix(x + pos_x, 0.5 + pos_y, 0.25 + pos_z).T)
        draw_elliptical_cylinder(a=0.03, b=0.03, height=0.5, color=support_color)
        glPopMatrix()
        
    # --- PERNAS DA CADEIRA ---
    for x in [-0.2, 0.2]:
        for z in [-0.2, 0.2]:
            glPushMatrix()
            glMultMatrixf(translation_matrix(x + pos_x, -0.0 + pos_y, z + pos_z).T)
            draw_elliptical_cylinder(a=0.07/2, b=0.07/2, height=0.5, color=support_color)
            glPopMatrix()