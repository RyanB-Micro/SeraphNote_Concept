import pygame
import nodes as nodes

# PyGame Settings
#-----------------
FPS = 60
pygame_running = False
screen = None
clock = None
font = None

# Display Colours
DARK_GREY = (123, 125, 123)
DARK_AZURE = (0, 105, 156)
BACK_AZURE = (16, 137, 180)
COOL_AZURE = (65, 174, 205)
SKY_AZURE = (172, 234, 255)
#ICON_GREY = (90, 76, 49)
SERAPH = (9*7, 1*7, 4*7)
CALM_AZURE = (70, 150, 153)


node_list = []
active_node = None

def create_node():
    global nodes
    node_list.append(nodes.Node(20, 20, SERAPH, "Test"))
    node_list.append(nodes.Node(80, 80, SERAPH, "Test"))


def draw_nodes():
    global node_list

    for node in node_list:
        #pygame.draw.rect(screen, node.colour, (node.x, node.y, node.width, node.height))
        pygame.draw.rect(screen, node.colour, node.box)
        text_surface = font.render(node.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (
                                node.x + (node.width / 2),
                                node.y + (node.height / 2)
                            )
        screen.blit(text_surface, text_rect)


def init_screen(WIDTH, HEIGHT):
    global clock, font, screen, pygame_running
    pygame.init()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("SeraphNote")
    pygame_running = True


def screen_loop():
    global clock, font, screen, pygame_running, active_node

    create_node()

    while pygame_running:
        for event in pygame.event.get():
            # Detect if window is being closed
            if event.type == pygame.QUIT:
                pygame_running = False

            # Clock timing
            delta_time = clock.tick(FPS) / 1000
            delta_time = max(0.001, min(0.1, delta_time))  # clamp for math error

            # blank screen
            screen.fill(CALM_AZURE)

            # Draw Nodes
            draw_nodes()
            # Check mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left mouse button
                    # check if mouse over box
                    for num, node in enumerate(node_list):
                        if node.box.collidepoint(event.pos):
                            active_node = node


            # move active node
            if event.type == pygame.MOUSEMOTION:
                if active_node != None:
                    active_node.set_position(event.pos[0], event.pos[1])
                    #active_node.box.move_ip(event.rel)


            # if mouse up, drop active box
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left mouse button
                    active_node = None


            pygame.draw.line(screen, DARK_GREY, (node_list[0].x, node_list[0].y), (node_list[1].x, node_list[1].y), 2)


        # Update screen
        pygame.display.flip()

    # Quit pygame on main loop finish
    pygame.quit()


if __name__ == '__main__':
    init_screen(1490, 914)
    screen_loop()