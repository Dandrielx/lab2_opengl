from OpenGL.GL import *
from matrices import translation_matrix
from renderer.tessellation import draw_tessellated_cuboid
from utils.materials import draw_cuboid
from utils.raster import bresenham_line

def draw_tables():
    table_top_color = (0.8, 0.1, 0.1, 1.0)
    leg_color = (0.1, 0.1, 0.1, 1.0)
    support_color = (0.05, 0.05, 0.05, 1.0)

    for row in range(-8, 10, 4):
        for col in range(-4, 9, 4):
            glPushMatrix()
            glMultMatrixf(translation_matrix(col, 1, row).T)

            # tampo
            glPushMatrix()
            draw_tessellated_cuboid((4, 0.1, 1.2), table_top_color, 128.0, (5, 1, 5))
            glPopMatrix()

            # perna
            glPushMatrix()
            glMultMatrixf(translation_matrix(-1.6, -0.5, 0).T)
            draw_cuboid((0.1, 0.9, 1.2), leg_color)
            glPopMatrix()

            # monitor 
            glPushMatrix()
            glMultMatrixf(translation_matrix(0, 0.5, -0.2).T) # tela
            draw_cuboid((1.2, 0.8, 0.05), support_color, 128)
            
            glMultMatrixf(translation_matrix(0, 0, -0.08).T) # tubo do monitor
            draw_cuboid((0.5, 0.3, 0.15), support_color, 128)
            
            glMultMatrixf(translation_matrix(0, -0.08, -0.12).T) # perna do monitor
            draw_cuboid((0.2, 0.8, 0.1), support_color, 128)
            
            glMultMatrixf(translation_matrix(0, -0.35, 0.1).T) # pé do monitor
            draw_cuboid((0.8, 0.02, 0.5), support_color, 128)
            
            glPopMatrix()

            glPopMatrix()

def draw_board():
    glPushMatrix()
    glMultMatrixf(translation_matrix(0, 2.5, -12.4).T)
    draw_cuboid((4, 2, 0.1), (1, 1, 1, 1), 10)

    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.1, 0.1)
    glPointSize(3.0)
    glBegin(GL_POINTS)

    for p in bresenham_line(0, 0, 100, 80):
        px = -1.9 + (p[0] / 100.0) * 3.8
        py = -0.9 + (p[1] / 80.0) * 1.8
        glVertex3f(px, py, 0.06)

    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()
