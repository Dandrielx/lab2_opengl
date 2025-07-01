from OpenGL.GL import *
from utils.materials import set_material
from matrices import translation_matrix, rotation_x, rotation_y, rotation_z
import numpy as np

def draw_tessellated_quad(width, height, divs_x, divs_y):
    """
    Desenha uma face 2D no plano XY, centrada na origem.
    A face é "tesselada", ou seja, subdividida em uma grade de faces menores.
    
    :width: Largura total da face no eixo X.
    :height: Altura total da face no eixo Y.
    :divs_x: Número de subdivisões na largura.
    :divs_y: Número de subdivisões na altura.
    """

    # Calcula as coordenadas de início e o tamanho de cada pequeno quad na grade.
    start_x, start_y = -width / 2, -height / 2
    step_x, step_y = width / divs_x, height / divs_y

   
    glNormal3f(0, 0, 1) # Define a normal para toda a face. Como ela é desenhada no plano XY,
                        # a normal aponta para o eixo Z positivo. A rotação será feita depois.

    glBegin(GL_QUADS)
    for i in range(divs_y):
        for j in range(divs_x):
            # Calcula os quatro cantos do pequeno quad atual.
            x0, y0 = start_x + j * step_x, start_y + i * step_y
            x1, y1 = x0 + step_x, y0 + step_y

             # Define os quatro vértices do quad.
            glVertex3f(x0, y0, 0)
            glVertex3f(x1, y0, 0)
            glVertex3f(x1, y1, 0)
            glVertex3f(x0, y1, 0)
    glEnd()


def draw_tessellated_cuboid(size, color, shininess, divisions):
    """
    Desenha um cuboide 3D completo, onde cada uma das 6 faces é tesselada em polígonos.
    Esta função funciona como um "montador": ela chama draw_tessellated_quad 6 vezes
    e usa matrizes de transformação para posicionar e rotacionar cada face no lugar certo.
    """
    w, h, d = size # Define as dimensões do cuboide.
    divs_x, divs_y, divs_z = divisions # Define as subdivisões.
    
    # Define as propriedades do material (cor, brilho) para todo o cuboide.
    set_material([c * 0.4 for c in color[:3]], color, [1, 1, 1, 1], shininess)

    # --- FACE DA FRENTE ---
    glPushMatrix()
    trans_mat = translation_matrix(0, 0, d / 2)
    glMultMatrixf(trans_mat.T) # .T transpõe a matriz para o formato do OpenGL
    draw_tessellated_quad(w, h, divs_x, divs_y)
    glPopMatrix()
    
    # --- FACE DA TRÁS ---
    glPushMatrix()
    trans_mat = translation_matrix(0, 0, -d / 2)
    rot_mat = rotation_y(180)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, h, divs_x, divs_y)
    glPopMatrix()
    
    # --- FACE DA ESQUERDA ---
    glPushMatrix()
    trans_mat = translation_matrix(-w / 2, 0, 0)
    rot_mat = rotation_y(-90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(d, h, divs_z, divs_y)
    glPopMatrix()
    
    # --- FACE DA DIREITA ---
    glPushMatrix()
    trans_mat = translation_matrix(w / 2, 0, 0)
    rot_mat = rotation_y(90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(d, h, divs_z, divs_y)
    glPopMatrix()

    # --- FACE DE CIMA ---
    glPushMatrix()
    trans_mat = translation_matrix(0, h / 2, 0)
    rot_mat = rotation_x(-90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, d, divs_x, divs_z)
    glPopMatrix()
    
    # --- FACE DE BAIXO ---
    glPushMatrix()
    trans_mat = translation_matrix(0, -h / 2, 0)
    rot_mat = rotation_x(90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, d, divs_x, divs_z)
    glPopMatrix()