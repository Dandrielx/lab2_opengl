from OpenGL.GL import *
from utils.materials import set_material
from matrices import translation_matrix, rotation_x, rotation_y, rotation_z
import numpy as np

def draw_tessellated_quad(width, height, divs_x, divs_y):
    start_x, start_y = -width / 2, -height / 2
    step_x, step_y = width / divs_x, height / divs_y
    glNormal3f(0, 0, 1)
    glBegin(GL_QUADS)
    for i in range(divs_y):
        for j in range(divs_x):
            x0, y0 = start_x + j * step_x, start_y + i * step_y
            x1, y1 = x0 + step_x, y0 + step_y
            glVertex3f(x0, y0, 0)
            glVertex3f(x1, y0, 0)
            glVertex3f(x1, y1, 0)
            glVertex3f(x0, y1, 0)
    glEnd()


def draw_tessellated_cuboid(size, color, shininess, divisions):
    w, h, d = size
    divs_x, divs_y, divs_z = divisions
    
    set_material([c * 0.4 for c in color[:3]], color, [1, 1, 1, 1], shininess)

    # Face da Frente
    glPushMatrix()
    trans_mat = translation_matrix(0, 0, d / 2)
    glMultMatrixf(trans_mat.T) # .T transpõe a matriz para o formato do OpenGL
    draw_tessellated_quad(w, h, divs_x, divs_y)
    glPopMatrix()
    
    # Face de Trás
    glPushMatrix()
    trans_mat = translation_matrix(0, 0, -d / 2)
    rot_mat = rotation_y(180)
    # A ordem importa: primeiro rotaciona, depois translada (lido da direita para a esquerda)
    # No código, multiplicamos na ordem inversa: Translação * Rotação
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, h, divs_x, divs_y)
    glPopMatrix()
    
    # Face da Esquerda
    glPushMatrix()
    trans_mat = translation_matrix(-w / 2, 0, 0)
    rot_mat = rotation_y(-90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(d, h, divs_z, divs_y)
    glPopMatrix()
    
    # Face da Direita
    glPushMatrix()
    trans_mat = translation_matrix(w / 2, 0, 0)
    rot_mat = rotation_y(90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(d, h, divs_z, divs_y)
    glPopMatrix()

    # Face de Cima
    glPushMatrix()
    trans_mat = translation_matrix(0, h / 2, 0)
    rot_mat = rotation_x(-90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, d, divs_x, divs_z)
    glPopMatrix()
    
    # Face de Baixo
    glPushMatrix()
    trans_mat = translation_matrix(0, -h / 2, 0)
    rot_mat = rotation_x(90)
    final_mat = np.dot(trans_mat, rot_mat)
    glMultMatrixf(final_mat.T)
    draw_tessellated_quad(w, d, divs_x, divs_z)
    glPopMatrix()