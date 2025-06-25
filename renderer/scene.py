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
from renderer.furniture import draw_tables, draw_board, draw_chair
from utils.materials import draw_cuboid


def draw_scene(camera, projection_mode):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if projection_mode == "perspective":
        glLoadMatrixf(perspective_matrix(50, (1280 / 720), 0.1, 100.0).T)
    else:
        glLoadMatrixf(orthographic_matrix(-10, 10, -5, 5, -10, 100).T)

    # Visão da câmera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.45, 0.45, 0.45, 1.0])

    # Luzes nas janelas
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

    # Aplica a câmera
    camera.get_view_matrix()

    # Piso
    floor_color = (0.7, 0.7, 0.6, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(0, -0.05, 0).T)
    draw_tessellated_cuboid((20, 0.1, 25), floor_color, 32.0, (5, 1, 5))
    glPopMatrix()
    
    # Parede do fundo
    wall_color = (0.9, 0.9, 0.85, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(0, 2.5, -12.5).T)
    draw_cuboid((20, 5, 0.1), wall_color)
    glPopMatrix()

    # Parede da direita
    glPushMatrix()
    glMultMatrixf(translation_matrix(10, 2.5, 0).T)
    draw_cuboid((0.1, 5, 25), wall_color)
    glPopMatrix()

    # Teto
    ceiling_color = (0.95, 0.95, 1.0, 1.0)
    glPushMatrix()
    glMultMatrixf(translation_matrix(0, 5.05, 0).T)
    draw_tessellated_cuboid((20, 0.1, 25), ceiling_color, 10.0, (5, 1, 5))
    glPopMatrix()

    # Parede com janelas
    draw_window_wall()

    # Mesas
    draw_tables()

    for row in range(-4, 12, 4):
        for col in range(-4, 16, 4):
            glPushMatrix()
            glMultMatrixf(translation_matrix(row, 0, col-2.5).T)
            glMultMatrixf(rotation_y(180).T)
            draw_chair()
            glPopMatrix()

    # Quadro branco com linha
    draw_board()
