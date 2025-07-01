from OpenGL.GL import *
import math

def draw_tampo(width, height, depth, corner_radius, segments):
    """
    Desenha o tampo da mesa com a borda longa de trás
    tendo seus dois cantos arredondados. A borda da frente é reta.
    """
    # Calcula as "meias" dimensões para facilitar o posicionamento centrado na origem.
    w2, h2, d2 = width / 2, height / 2, depth / 2 
    
    perimeter_vertices = [] # Pré-calculo dos vértices do perímetro superior.
    perimeter_vertices.append((-w2, -d2)) # Canto reto frontal-esquerdo.
    perimeter_vertices.append((w2, -d2)) # Canto reto frontal-direito.
    perimeter_vertices.append((w2, d2 - corner_radius)) # Início do canto traseiro-direito.

    # Gera os pontos para o canto arredondado traseiro-direito
    center_x, center_z = w2 - corner_radius, d2 - corner_radius
    for i in range(segments + 1):
        angle = (math.pi / 2) * i / segments # De 0 a 90 graus
        perimeter_vertices.append((center_x + corner_radius * math.cos(angle),
                                   center_z + corner_radius * math.sin(angle)))

    # Início do canto traseiro-esquerdo
    perimeter_vertices.append((-w2 + corner_radius, d2))

    # Gera os pontos para o canto arredondado traseiro-esquerdo
    center_x, center_z = -w2 + corner_radius, d2 - corner_radius
    for i in range(segments + 1):
        angle = math.pi / 2 + (math.pi / 2) * i / segments # De 90 a 180 graus
        perimeter_vertices.append((center_x + corner_radius * math.cos(angle),
                                   center_z + corner_radius * math.sin(angle)))

    # --- DESENHAR A FACE SUPERIOR ---
    glNormal3f(0, 1, 0) # Define a normal que aponta para cima, perpendicular a toda a face.
    glBegin(GL_POLYGON) # Usa GL_POLYGON para criar uma única face preenchida a partir da lista de vértices.
    for x, z in perimeter_vertices:
        glVertex3f(x, h2, z)
    glEnd()

    # --- DESENHAR A FACE INFERIOR ---
    glNormal3f(0, -1, 0) # A normal agora aponta para baixo.
    glBegin(GL_POLYGON) # A lista de vértices é percorrida em ordem REVERSA. Isso é crucial para que
                        # a face "aponte" para baixo, garantindo que a iluminação seja calculada corretamente.
    for x, z in reversed(perimeter_vertices):
        glVertex3f(x, -h2, z)
    glEnd()

    # --- DESENHAR AS LATERAIS ---
    glBegin(GL_QUAD_STRIP) # GL_QUAD_STRIP é uma primitiva eficiente para desenhar uma "casca" ou "fita"

    # Itera sobre os vértices do perímetro para criar a parede lateral.
    for i in range(len(perimeter_vertices)):
        x1, z1 = perimeter_vertices[i]
        # Pega o vértice anterior para calcular o vetor da aresta.
        x2, z2 = perimeter_vertices[(i - 1 + len(perimeter_vertices)) % len(perimeter_vertices)]
        
        edge_vec = (x1 - x2, z1 - z2) # Calcula a direção da aresta atual.
        normal = (edge_vec[1], 0, -edge_vec[0]) # Esta normal aponta para "fora" da lateral do tampo.
        norm = math.sqrt(normal[0]**2 + normal[2]**2) # Normalizar o vetor
        if norm > 0:
            glNormal3f(normal[0]/norm, 0, normal[2]/norm)
        
        glVertex3f(x1, -h2, z1) # Para cada ponto no perímetro, define um vértice inferior e um superior,
                                # criando um segmento vertical da parede lateral.
        glVertex3f(x1, h2, z1)

    # Adiciona o primeiro par de vértices novamente para fechar o loop.
    x1, z1 = perimeter_vertices[0]
    glVertex3f(x1, -h2, z1)
    glVertex3f(x1, h2, z1)
    glEnd()

def set_material(ambient, diffuse, specular, shininess):
    """Função auxiliar para centralizar a configuração do material de um objeto."""
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

def draw_cuboid(size, color, shininess=32.0):
    """Desenha um cuboide simples, alinhado aos eixos e centrado na origem."""
    w, h, d = size[0] / 2, size[1] / 2, size[2] / 2 

    # Calcula uma cor ambiente um pouco mais escura que a cor principal.
    ambient_color = [c * 0.4 for c in color[:3]] + [color[3]] if len(color) == 4 else [c * 0.4 for c in color]  
    set_material(ambient_color, color, [1, 1, 1, 1], shininess)

    # Define os 8 vértices do cubo.
    vertices = [(w, h, -d), (w, -h, -d), (-w, -h, -d), (-w, h, -d), (w, h, d), (w, -h, d), (-w, -h, d), (-w, h, d)]

    # Define as 6 normais, uma para cada face, apontando para fora.
    normals = [(0, 0, -1), (0, 0, 1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

    # Define quais vértices compõem cada uma das 6 faces.
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 3, 7, 4), (1, 5, 6, 2), (0, 4, 5, 1), (3, 2, 6, 7)]
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i]) # Define a normal para a face que será desenhada.
        for vertex_index in face: # Desenha os 4 vértices da face.
            glVertex3fv(vertices[vertex_index])
    glEnd()

def draw_elliptical_cylinder(a, b, height, slices=36, color=(0.5, 0.5, 0.9, 1.0),
                              specular=(0.2, 0.2, 0.2, 1.0), shininess=8.0):
    
    """Desenha um cilindro com base elíptica."""
    ambient_color = [c * 0.4 for c in color[:3]] + [color[3]]
    set_material(ambient_color, color, specular, shininess)

    glBegin(GL_QUAD_STRIP) # Desenha as faces laterais curvas usando um QUAD_STRIP.
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)

        # A normal em uma superfície curva aponta radialmente para fora do centro.
        # Isso garante uma iluminação suave e arredondada.
        glNormal3f(x, 0, z)

        # Define um par de vértices para criar um segmento da parede.
        glVertex3f(x, 0, z)
        glVertex3f(x, height, z)
    glEnd()

    # Desenha a "tampa" de baixo usando um TRIANGLE_FAN.
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, -1, 0) # Normal aponta para baixo.
    glVertex3f(0, 0, 0)  # Vértice central do leque.
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)
        glVertex3f(x, 0, z) # Vértices da borda da elipse.
    glEnd()

    # Desenha a "tampa" de cima.
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 1, 0) # Normal aponta para cima.
    glVertex3f(0, height, 0) # Vértice central do leque.
    for i in range(slices + 1):
        theta = 2 * math.pi * i / slices
        x = a * math.cos(theta)
        z = b * math.sin(theta)
        glVertex3f(x, height, z) # Vértices da borda da elipse.
    glEnd()