import pygame
import nodes as nodes

# PyGame Settings
#-----------------
FPS = 60
pygame_running = False
screen = None
clock = None
font = None
font_small = None

# Display Colours
DARK_GREY = (123, 125, 123)
DARK_AZURE = (0, 105, 156)
BACK_AZURE = (16, 137, 180)
COOL_AZURE = (65, 174, 205)
SKY_AZURE = (172, 234, 255)
#ICON_GREY = (90, 76, 49)
SERAPH = (9*7, 1*7, 4*7)
CALM_AZURE = (70, 150, 153)
CHILL_GREY = (102, 153, 153)
LINE_MAKE = (102, 153, 153)


node_list = []
bond_list = []
draggable_node = None
build_line = False
initial_corner = None
terminate_corner = None
changeable_node = None
changeable_bond = None




def create_node():
    global nodes
    node_list.append(nodes.Node(20, 20, SERAPH, "Test 1"))
    node_list.append(nodes.Node(80, 80, SERAPH, "Test 2"))
    node_list.append(nodes.Node(100, 220, SERAPH, "Test 3"))
    node_list.append(nodes.Node(280, 200, SERAPH, "Test 4"))


# def draw_tool_box():
#     tool_box = pygame.Rect(0, 0, 35, 15)

def draw_nodes():
    global node_list

    for num, node in enumerate(node_list):
        #pygame.draw.rect(screen, node.colour, (node.x, node.y, node.width, node.height))

        if num == changeable_node:
            pygame.draw.rect(screen, DARK_GREY, node.box)
        else:
            pygame.draw.rect(screen, node.colour, node.box)

        label_text = font.render(node.text, True, (255, 255, 255))
        label_rect = label_text.get_rect()
        label_rect.center = (
                                node.x + (node.width / 2),
                                node.y + ((node.height / 5) * 2)
                            )
        screen.blit(label_text, label_rect)

        id_text = font_small.render(node.id, True, (255, 255, 255))
        id_rect = id_text.get_rect()
        id_rect.center = (
            node.x + (node.width / 2),
            node.y + ((node.height / 5) * 4)
        )
        screen.blit(id_text, id_rect)

        for corner in node.corners:
            pygame.draw.circle(screen, DARK_AZURE, corner, 5)



def draw_bonds():
    for num, bond in enumerate(bond_list):
        bond.update_position()

        # Draw bond line
        pygame.draw.line(screen, SKY_AZURE, (bond.x, bond.y), (bond.term_x, bond.term_y), 2)

        # Draw id box
        # id_box = pygame.Rect(0, 0, 35, 15)
        # id_box.center = (
        #     ((bond.x + bond.term_x) / 2),
        #     ((bond.y + bond.term_y) / 2)
        # )
        if num == changeable_bond:
            pygame.draw.rect(screen, LINE_MAKE, bond.id_box)
        else:
            pygame.draw.rect(screen, BACK_AZURE, bond.id_box)

        # Draw id
        id_text = font_small.render(bond.id, True, (0, 0, 0))
        id_rect = id_text.get_rect()
        id_rect.center = (
            ((bond.x + bond.term_x) / 2),
            ((bond.y + bond.term_y) / 2)
        )
        screen.blit(id_text, id_rect)

        # Draw text
        label_text = font.render(bond.text, True, (255-7, 255-7, 255-7))
        label_rect = label_text.get_rect()
        label_rect.center = (
            ((bond.x + bond.term_x) / 2),
            ((bond.y + bond.term_y) / 2) - 20
        )
        screen.blit(label_text, label_rect)





def init_screen(WIDTH, HEIGHT):
    global clock, font, font_small, screen, pygame_running
    pygame.init()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    font_small = pygame.font.SysFont(None, 16)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("SeraphNote")
    pygame_running = True


def line_builder(original_corner, mouse_x, mouse_y):
    node = original_corner[0]
    corner_num = original_corner[1]
    corner_x = node.corners[corner_num][0]
    corner_y = node.corners[corner_num][1]

    pygame.draw.line(screen, DARK_GREY, (corner_x, corner_y), (mouse_x, mouse_y), 2)


def bond_builder(original_corner, end_corner, mouse_x, mouse_y):
    global bond_list
    node_1 = original_corner[0]
    corner_1_num = original_corner[1]
    # corner_1_x = node_1.corners[corner_1_num][0]
    # corner_1_y = node_1.corners[corner_1_num][1]

    node_2 = end_corner[0]
    corner_2_num = end_corner[1]
    # corner_2_x = node_2.corners[corner_2_num][0]
    # corner_2_y = node_2.corners[corner_2_num][1]

    bond = nodes.Bond(node_1, node_2, corner_1_num, corner_2_num)
    bond_list.append(bond)




def screen_loop():
    global clock, font, screen, pygame_running, draggable_node, build_line,\
        initial_corner, terminate_corner, changeable_node, changeable_bond

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
            draw_bonds()


            # Check mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left mouse button
                    # check if mouse over box
                    for num, node in enumerate(node_list):
                        # check if box selected
                        if node.box.collidepoint(event.pos):
                            changeable_node = num
                        # check if circle selected
                        for i, corner in enumerate(node.corners):
                            # if within radius of the circle
                            if ((event.pos[0] - corner[0]) ** 2 + (event.pos[1] - corner[1]) ** 2) <= 25:
                                if build_line == False: # Start making line
                                    build_line = True
                                    initial_corner = (node, i)
                                else: # finish making line
                                    build_line = False
                                    terminate_corner = (node, i)

                    # check if over bond
                    for num, bond in enumerate(bond_list):
                        if bond.id_box.collidepoint(event.pos):
                            changeable_bond = num

                if event.button == 3: # right mouse button
                    # check if mouse over box
                    for num, node in enumerate(node_list):
                        # check if box selected
                        if node.box.collidepoint(event.pos):
                            draggable_node = node




            # move active node
            if event.type == pygame.MOUSEMOTION:
                if draggable_node != None:
                    draggable_node.set_position(event.pos[0], event.pos[1])
                if build_line:
                    line_builder(initial_corner, event.pos[0], event.pos[1])
                if terminate_corner:
                    bond_builder(initial_corner, terminate_corner, event.pos[0], event.pos[1])
                    initial_corner = None
                    terminate_corner = None


            # if mouse up, drop active box
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # right mouse button
                    draggable_node = None


            #pygame.draw.line(screen, DARK_GREY, (node_list[0].x, node_list[0].y), (node_list[1].x, node_list[1].y), 2)


        # Update screen
        pygame.display.flip()

    # Quit pygame on main loop finish
    pygame.quit()



if __name__ == '__main__':
    init_screen(1490, 914)
    screen_loop()