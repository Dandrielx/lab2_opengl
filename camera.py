import numpy as np
import math
from OpenGL.GLU import gluLookAt

class Camera:
    def __init__(self, position=(0, 1.7, 10), yaw=-90, pitch=0):
        self.position = np.array(position, dtype=np.float32)
        self.yaw = yaw
        self.pitch = pitch
        self.update_vectors()

    def update_vectors(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        self.front = np.array([math.cos(yaw_rad) * math.cos(pitch_rad), math.sin(pitch_rad), math.sin(yaw_rad) * math.cos(pitch_rad)])
        self.front /= np.linalg.norm(self.front)
        world_up = np.array([0, 1, 0])
        self.right = np.cross(self.front, world_up)
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up /= np.linalg.norm(self.up)

    def process_mouse_movement(self, xoffset, yoffset, sensitivity=0.1):
        self.yaw += xoffset * sensitivity
        self.pitch -= yoffset * sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_vectors()

    def process_keyboard(self, direction, speed):
        if direction == 'FORWARD': self.position += self.front * speed
        if direction == 'BACKWARD': self.position -= self.front * speed
        if direction == 'LEFT': self.position -= self.right * speed
        if direction == 'RIGHT': self.position += self.right * speed

    def get_view_matrix(self):
        target = self.position + self.front
        return gluLookAt(self.position[0], self.position[1], self.position[2], target[0], target[1], target[2], self.up[0], self.up[1], self.up[2])
