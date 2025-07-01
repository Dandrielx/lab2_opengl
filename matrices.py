import numpy as np
import math

# --- MATRIX PARA TRANSLAÇÃO DO OBJETO --- 
def translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- MATRIX PARA MODIFICAÇÃO DE ESCALA --- 
def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- MATRIX PARA ROTAÇÃO NO EIXO X --- 
def rotation_x(angle_degrees):
    angle_rad = math.radians(angle_degrees)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- MATRIX PARA ROTAÇÃO NO EIXO Y --- 
def rotation_y(angle_degrees):
    angle_rad = math.radians(angle_degrees)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- MATRIX PARA ROTAÇÃO NO EIXO Z --- 
def rotation_z(angle_degrees):
    angle_rad = math.radians(angle_degrees)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

# --- MATRIX PARA VISTA EM PERSPECTIVA --- 
def perspective_matrix(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2)
    return np.array([[f / aspect, 0, 0, 0], 
                     [0, f, 0, 0], 
                     [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)], 
                     [0, 0, -1, 0]], dtype=np.float32)

# --- MATRIX PARA VISTA ORTOGRÁFICA --- 
def orthographic_matrix(left, right, bottom, top, near, far):
    return np.array([[2 / (right - left), 0, 0, -(right + left) / (right - left)], 
                     [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)], 
                     [0, 0, -2 / (far - near), -(far + near) / (far - near)], 
                     [0, 0, 0, 1]], dtype=np.float32)
