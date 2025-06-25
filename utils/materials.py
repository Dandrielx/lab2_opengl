from OpenGL.GL import *
import math

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

def draw_elliptical_cylinder(a, b, height, slices=36, color=(0.5, 0.5, 0.9, 1.0), shininess=32.0): # Add shininess parameter
    """Desenha uma elipse em pé (cilindro elíptico vertical ou horizontal)."""
    
    # Calculate ambient color similar to draw_cuboid
    ambient_color = [c * 0.4 for c in color[:3]] + [color[3]] if len(color) == 4 else [c * 0.4 for c in color]
    set_material(ambient_color, color, [1, 1, 1, 1], shininess) # Set material properties

    # Side faces
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)
        glNormal3f(x, 0, z) # Normals for the sides
        glVertex3f(x, 0, z)
        glVertex3f(x, height, z)
    glEnd()

    # Bottom cap
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, -1, 0) # Normal for the bottom cap
    glVertex3f(0, 0, 0)
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)
        glVertex3f(x, 0, z)
    glEnd()

    # Top cap
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 1, 0) # Normal for the top cap
    glVertex3f(0, height, 0)
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)
        glVertex3f(x, height, z)
    glEnd()