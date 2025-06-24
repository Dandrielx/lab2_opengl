import pygame
from pygame.locals import *
from OpenGL.GL import *
from camera import Camera
from renderer.scene import draw_scene

def main():
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulação de Sala")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glClearColor(0.6, 0.8, 1.0, 1.0)

    camera = Camera()
    clock = pygame.time.Clock()
    pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
    last_x, last_y = pygame.mouse.get_pos()
    projection_mode = 'perspective'
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                projection_mode = 'perspective' if projection_mode == 'orthographic' else 'orthographic'

        keys = pygame.key.get_pressed()
        cam_speed = 5.0 * dt
        if keys[pygame.K_w]: camera.process_keyboard('FORWARD', cam_speed)
        if keys[pygame.K_s]: camera.process_keyboard('BACKWARD', cam_speed)
        if keys[pygame.K_a]: camera.process_keyboard('LEFT', cam_speed)
        if keys[pygame.K_d]: camera.process_keyboard('RIGHT', cam_speed)

        curr_x, curr_y = pygame.mouse.get_pos()
        x_offset, y_offset = curr_x - last_x, curr_y - last_y
        pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
        last_x, last_y = display[0] // 2, display[1] // 2
        camera.process_mouse_movement(x_offset, y_offset)

        draw_scene(camera, projection_mode)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
