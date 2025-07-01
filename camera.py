import numpy as np
import math
from OpenGL.GLU import gluLookAt

class Camera:
    def __init__(self, position=(0, 1.7, 10), yaw=-90, pitch=0):
        """
        :position: Posição inicial da câmera no mundo.
        :yaw: Rotação inicial em torno do eixo Y (olhar para esquerda/direita).
        :pitch: Rotação inicial em torno do eixo X (olhar para cima/baixo).
        """
        self.position = np.array(position, dtype=np.float32)
        self.yaw = yaw
        self.pitch = pitch
        self.update_vectors()

    def update_vectors(self):
        """
        Calcula os vetores direcionais (front, right, up) com base nos ângulos yaw e pitch.
        Este método é chamado sempre que o yaw ou o pitch mudarem.
        """
        # Converte os ângulos de graus para radianos.
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        # Calcula o novo vetor 'front' usando trigonometria esférica.
        # Este vetor aponta para a direção que a câmera está olhando.
        front_vector = np.array([
            math.cos(yaw_rad) * math.cos(pitch_rad),
            math.sin(pitch_rad),
            math.sin(yaw_rad) * math.cos(pitch_rad)
        ])
       
        self.front = front_vector / np.linalg.norm(front_vector) # Normaliza o vetor.
        
       
        world_up = np.array([0, 1, 0]) # Define um vetor 'up' global para o mundo. Usado como referência para calcular o vetor 'right'.

        # Calcula o vetor 'right' usando o produto vetorial entre 'front' e 'world_up'.
        # O resultado é um vetor perpendicular a ambos, apontando para a direita da câmera.
        self.right = np.cross(self.front, world_up)
        self.right /= np.linalg.norm(self.right) # Normaliza o vetor 'right'.
        
        # Calcula o vetor 'up' real da câmera com base nos vetores 'right' e 'front'.
        # Garante que os três vetores (front, right, up) sejam sempre perpendiculares entre si.
        self.up = np.cross(self.right, self.front)
        self.up /= np.linalg.norm(self.up) # Normaliza o vetor 'up'.

    def process_mouse_movement(self, xoffset, yoffset, sensitivity=0.1):
        """
        :xoffset: Deslocamento do mouse no eixo X.
        :yoffset: Deslocamento do mouse no eixo Y.
        :sensitivity: Multiplicador para controlar a velocidade da rotação.
        """
        # Atualiza o yaw e o pitch com base no deslocamento do mouse e na sensibilidade.
        self.yaw += xoffset * sensitivity
        self.pitch -= yoffset * sensitivity
        
        # Limita o pitch entre -89 e 89 graus para evitar que a câmera "vire de cabeça para baixo".
        self.pitch = max(-89.0, min(89.0, self.pitch))
        
        # Recalcula os vetores direcionais com a nova orientação.
        self.update_vectors()

    def process_keyboard(self, direction, speed):
        """
        :direction: String que indica a direção do movimento.
        :speed: A distância que a câmera deve se mover no quadro.
        """
        # Move a posição da câmera adicionando ou subtraindo os vetores direcionais.
        if direction == 'FORWARD': self.position += self.front * speed
        if direction == 'BACKWARD': self.position -= self.front * speed
        if direction == 'LEFT': self.position -= self.right * speed
        if direction == 'RIGHT': self.position += self.right * speed

    def get_view_matrix(self):
        """
        Calcula e aplica a matriz de visão usando gluLookAt.
        Posiciona o "olho" do OpenGL de acordo com o estado da câmera.
        """
        # Calcula o ponto para o qual a câmera está olhando.
        target = self.position + self.front
        
        # Chama gluLookAt, que modifica a matriz GL_MODELVIEW atual do OpenGL.
        # Parâmetros: (posição do olho), (ponto alvo), (vetor 'up' da câmera).
        return gluLookAt(
            self.position[0], self.position[1], self.position[2],
            target[0], target[1], target[2],
            self.up[0], self.up[1], self.up[2]
        )