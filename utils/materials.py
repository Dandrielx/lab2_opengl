from OpenGL.GL import *

def set_material(ambient, diffuse, specular, shininess):
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

def draw_cuboid(size, color, shininess=32.0):
    w, h, d = size[0] / 2, size[1] / 2, size[2] / 2
    ambient_color = [c * 0.4 for c in color[:3]] + [color[3]] if len(color) == 4 else [c * 0.4 for c in color]
    set_material(ambient_color, color, [1, 1, 1, 1], shininess)
    vertices = [(w, h, -d), (w, -h, -d), (-w, -h, -d), (-w, h, -d), (w, h, d), (w, -h, d), (-w, -h, d), (-w, h, d)]
    normals = [(0, 0, -1), (0, 0, 1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 3, 7, 4), (1, 5, 6, 2), (0, 4, 5, 1), (3, 2, 6, 7)]
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for vertex_index in face:
            glVertex3fv(vertices[vertex_index])
    glEnd()
