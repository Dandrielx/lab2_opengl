from OpenGL.GL import *
import math

def draw_tampo(width, height, depth, corner_radius, segments):
    """
    (VERSÃO DEFINITIVA) Desenha o tampo da mesa com a borda longa de trás
    tendo seus dois cantos arredondados. A borda da frente é reta.
    """
    w2, h2, d2 = width / 2, height / 2, depth / 2
    
    # --- 1. Pré-calcular os vértices do perímetro superior ---
    perimeter_vertices = []
    
    # Canto reto frontal-esquerdo
    perimeter_vertices.append((-w2, -d2))
    
    # Canto reto frontal-direito
    perimeter_vertices.append((w2, -d2))

    # Início do canto traseiro-direito
    perimeter_vertices.append((w2, d2 - corner_radius))

    # Canto arredondado traseiro-direito
    center_x, center_z = w2 - corner_radius, d2 - corner_radius
    for i in range(segments + 1):
        angle = (math.pi / 2) * i / segments # De 0 a 90 graus
        perimeter_vertices.append((center_x + corner_radius * math.cos(angle),
                                   center_z + corner_radius * math.sin(angle)))

    # Início do canto traseiro-esquerdo
    perimeter_vertices.append((-w2 + corner_radius, d2))

    # Canto arredondado traseiro-esquerdo
    center_x, center_z = -w2 + corner_radius, d2 - corner_radius
    for i in range(segments + 1):
        angle = math.pi / 2 + (math.pi / 2) * i / segments # De 90 a 180 graus
        perimeter_vertices.append((center_x + corner_radius * math.cos(angle),
                                   center_z + corner_radius * math.sin(angle)))

    # --- 2. Desenhar a Face Superior ---
    glNormal3f(0, 1, 0)
    glBegin(GL_POLYGON)
    for x, z in perimeter_vertices:
        glVertex3f(x, h2, z)
    glEnd()

    # --- 3. Desenhar a Face Inferior ---
    glNormal3f(0, -1, 0)
    glBegin(GL_POLYGON)
    for x, z in reversed(perimeter_vertices):
        glVertex3f(x, -h2, z)
    glEnd()

    # --- 4. Desenhar as Laterais ---
    glBegin(GL_QUAD_STRIP)
    # Gerando a "casca" lateral a partir do perímetro
    for i in range(len(perimeter_vertices)):
        x1, z1 = perimeter_vertices[i]
        x2, z2 = perimeter_vertices[(i - 1 + len(perimeter_vertices)) % len(perimeter_vertices)]
        
        # Vetor da aresta
        edge_vec = (x1 - x2, z1 - z2)
        # Normal da face lateral (perpendicular à aresta no plano XZ)
        normal = (edge_vec[1], 0, -edge_vec[0])
        # Normalizar o vetor
        norm = math.sqrt(normal[0]**2 + normal[2]**2)
        if norm > 0:
            glNormal3f(normal[0]/norm, 0, normal[2]/norm)
        
        glVertex3f(x1, -h2, z1)
        glVertex3f(x1, h2, z1)

    # Fechar o quad strip
    x1, z1 = perimeter_vertices[0]
    glVertex3f(x1, -h2, z1)
    glVertex3f(x1, h2, z1)
    glEnd()

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

def draw_elliptical_cylinder(a, b, height, slices=36, color=(0.5, 0.5, 0.9, 1.0),
                              specular=(0.2, 0.2, 0.2, 1.0), shininess=8.0):
    ambient_color = [c * 0.4 for c in color[:3]] + [color[3]]
    set_material(ambient_color, color, specular, shininess) # Set material properties

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