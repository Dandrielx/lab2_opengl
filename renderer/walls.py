from OpenGL.GL import *
from matrices import create_translation_matrix
from utils.materials import draw_cuboid

def draw_window_wall():
    wall_color = (0.9, 0.9, 0.85, 1.0)
    window_height = 3.0
    window_base_y = 1.0
    wall_x = -10.0

    # Parte de baixo da parede
    glPushMatrix()
    glMultMatrixf(create_translation_matrix(wall_x, window_base_y / 2, 0).T)
    draw_cuboid((0.2, window_base_y, 25), wall_color)
    glPopMatrix()

    # Parte de cima da parede
    glPushMatrix()
    glMultMatrixf(create_translation_matrix(wall_x, window_base_y + window_height + (5.0 - window_base_y - window_height) / 2, 0).T)
    draw_cuboid((0.2, 5.0 - window_base_y - window_height, 25), wall_color)
    glPopMatrix()

    # Pilares entre as janelas
    pillars = [{'z_pos': -3.0, 'width': 2}, {'z_pos': 4.0, 'width': 2}]
    for p in pillars:
        glPushMatrix()
        glMultMatrixf(create_translation_matrix(wall_x, window_base_y + window_height / 2, p['z_pos']).T)
        draw_cuboid((0.2, window_height, p['width']), wall_color)
        glPopMatrix()

    # Vidros das janelas (com transparência)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glass_color = [0.8, 0.9, 1.0, 0.3]
    windows = [{'z_pos': -7.0, 'width': 4}, {'z_pos': 0.0, 'width': 4}, {'z_pos': 7.0, 'width': 4}]
    for w in windows:
        glPushMatrix()
        glMultMatrixf(create_translation_matrix(wall_x, window_base_y + window_height / 2, w['z_pos']).T)
        draw_cuboid((0.05, window_height, w['width']), glass_color, 100)
        glPopMatrix()
    glDisable(GL_BLEND)
