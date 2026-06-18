import pygame
import nodes as nodes
import pandas as pd

WIDTH = 1490
HEIGHT = 914

# PyGame Settings
#-----------------
FPS = 60
pygame_running = False
screen = None
clock = None
font_big = None
font_big_italic = None
font = None
font_bold = None
font_bold_italic = None
font_small = None
pygame_version = pygame.version.ver

# Display Colours
DARK_GREY = (123, 125, 123)
MID_GREY = (194, 194, 194)
DARK_AZURE = (0, 105, 156)
BACK_AZURE = (16, 137, 180)
COOL_AZURE = (65, 174, 205)
SKY_AZURE = (172, 234, 255)
#ICON_GREY = (90, 76, 49)
SERAPH = (9*7, 1*7, 4*7)
CALM_AZURE = (70, 150, 153)
CHILL_GREY = (102, 153, 153)
LINE_MAKE = (102, 153, 153)
MID_YELLOW = (255, 194, 49)
LIGHT_YELLOW = (255, 255, 149)
POINT_BLUE = (81, 181, 255)
VISION_AZURE = (7+(9+1+4), 7*(9+1+4), 7*(9+1+4))


node_list = []
fact_list = []
bond_list = []
tools_list = []
tool_choices = [("New Node", SERAPH), ("New Fact", VISION_AZURE), ("New Source", CHILL_GREY), ("New Quote", LINE_MAKE)]
draggable_node = None
draggable_fact = None
build_line = False
initial_corner = None
terminate_corner = None
changeable_node = None
changeable_bond = None
changeable_fact = None
selected_tool = None
cursor_colour = VISION_AZURE


tool_strip_width = 64
tool_width = 100
tool_height = 50
tool_spacing = 20

window_title = "SeraphNote"




def create_node():
    global nodes
    node_list.append(nodes.Node(20, 20, SERAPH, "Test 1"))
    node_list.append(nodes.Node(80, 80, SERAPH, "Test 2"))
    node_list.append(nodes.Node(100, 220, SERAPH, "Test 3"))
    node_list.append(nodes.Node(280, 200, SERAPH, "Test 4"))


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


def draw_facts():
    global fact_list

    for num, fact in enumerate(fact_list):
        #pygame.draw.rect(screen, node.colour, (node.x, node.y, node.width, node.height))

        if num == changeable_fact:
            pygame.draw.rect(screen, DARK_GREY, fact.box, border_radius=7)
        else:
            pygame.draw.rect(screen, fact.colour, fact.box, border_radius=7)

        label_text = font.render(fact.title, True, (255, 255, 255))
        label_rect = label_text.get_rect()
        label_rect.center = (
                                fact.x + (fact.width / 2),
                                fact.y + ((fact.height / 7) * 1)
                            )
        screen.blit(label_text, label_rect)

        body_text = font_small.render(fact.text, True, (255, 255, 255))
        body_rect = body_text.get_rect()
        body_rect.center = (
            fact.x + (fact.width / 2),
            fact.y + ((fact.height / 7) * 2)
        )
        screen.blit(body_text, body_rect)


        id_text = font_small.render(fact.id, True, (255, 255, 255))
        id_rect = id_text.get_rect()
        id_rect.center = (
            fact.x + (fact.width / 2),
            fact.y + ((fact.height / 7) * 6)
        )
        screen.blit(id_text, id_rect)

        for corner in fact.corners:
            pygame.draw.circle(screen, DARK_AZURE, corner, 5)



def draw_bonds():
    for num, bond in enumerate(bond_list):
        bond.update_position()

        # Defualt direction of points arrow
        points = [(bond.term_x - 7, bond.term_y - 7), (bond.term_x - 7, bond.term_y + 7),
                  (bond.term_x, bond.term_y)]

        # Draw bond line
        pygame.draw.line(screen, SKY_AZURE, (bond.x, bond.y), (bond.term_x, bond.term_y), 2)

        # draw terminating direction arrow
        if bond.x > bond.term_x:
            points = [(bond.term_x + 7, bond.term_y - 7), (bond.term_x + 7, bond.term_y + 7),
                      (bond.term_x, bond.term_y)]

        # Draw terminating arrow
        #pygame.draw.polygon(screen, COOL_AZURE, points, width=0)
        pygame.draw.polygon(screen, POINT_BLUE, points, width=0)

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
    global clock, font_big, font, font_small, screen, pygame_running, pygame_version, font_bold_italic, font_big_italic, font_bold
    pygame.init()

    pygame_version = pygame.version.ver

    clock = pygame.time.Clock()
    font_big_italic = pygame.font.SysFont(None, 50, italic=True)
    font_big = pygame.font.SysFont(None, 50)
    font = pygame.font.SysFont(None, 20)
    font_bold = pygame.font.SysFont(None, 20, bold=True)
    font_bold_italic = pygame.font.SysFont(None, 20, italic=True, bold=True)
    font_small = pygame.font.SysFont(None, 16)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("SeraphNote")
    pygame_running = True

    create_toolstrip()


def line_builder(original_corner, mouse_x, mouse_y):
    if build_line is not None:
        node = original_corner[0]
        corner_num = original_corner[1]
        corner_x = node.corners[corner_num][0]
        corner_y = node.corners[corner_num][1]

        pygame.draw.line(screen, DARK_GREY, (corner_x, corner_y), (mouse_x, mouse_y), 2)


def bond_builder(original_corner, end_corner, mouse_x, mouse_y):
    global bond_list
    if terminate_corner is not None:
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




def create_toolstrip():
    global tools_list

    tools_list.clear()

    for i in range(len(tool_choices)):
        tool_buffer = pygame.Rect(0, 0, tool_width, tool_height)
        tool_buffer.center = (
            ((i * tool_width) + i*tool_spacing) + tool_width,
            ((HEIGHT - tool_strip_width) + (tool_height/2))
        )
        tools_list.append(tool_buffer)



def draw_toolstrip():
    tool_strip_colour = SKY_AZURE#COOL_AZURE
    if selected_tool == 0:
        tool_strip_colour = SERAPH
    if selected_tool == 1:
        tool_strip_colour = VISION_AZURE
    pygame.draw.rect(screen, tool_strip_colour, (0, HEIGHT - tool_strip_width - 10, WIDTH, HEIGHT))


    tool_strip_box = pygame.Rect(0, HEIGHT - tool_strip_width, WIDTH, HEIGHT)
    pygame.draw.rect(screen, DARK_GREY, tool_strip_box)

    for i, tool in enumerate(tools_list):
        pygame.draw.rect(screen, tool_choices[i][1], tool)

        # Draw text
        label_text = font.render(tool_choices[i][0], True, (255 - 7, 255 - 7, 255 - 7))
        label_rect = label_text.get_rect()
        label_rect.center = (
            ((i * tool_width) + i * tool_spacing) + tool_width,
            ((HEIGHT - tool_strip_width) + (tool_height / 2))
        )
        screen.blit(label_text, label_rect)


    # Draw window text
    main_text = font_big_italic.render("SeraphNote", True, (255 - 7, 255 - 7, 255 - 7))
    main_text_rect = main_text.get_rect()
    main_text_rect.center = (1280, 875)
    screen.blit(main_text, main_text_rect)

    slogan_text = font_bold.render("Connecting Facts to Thoughts", True, tool_strip_colour)
    slogan_text_rect = slogan_text.get_rect()
    slogan_text_rect.center = (1320, 900)
    screen.blit(slogan_text, slogan_text_rect)


def delete_item(item, item_list):
    if item in item_list:
        item_list.remove(item)

    # search if item connected to any bonds
    effected_bonds = []
    for bond in bond_list:
        if bond.node_1 == item or bond.node_2 == item:
            effected_bonds.append(bond)

    # remove any effected bonds
    for bond in effected_bonds:
        bond_list.remove(bond)


def delete_bond(bond):
    bond_list.remove(bond)




def screen_loop():
    global clock, font, screen, pygame_running, draggable_node, build_line,\
        initial_corner, terminate_corner, changeable_node, changeable_bond, \
        selected_tool, cursor_colour, draggable_fact, changeable_fact

    #create_node()
    #create_toolstrip()

    while pygame_running:
        # Clock timing
        delta_time = clock.tick(FPS) / 1000
        delta_time = max(0.001, min(0.1, delta_time))  # clamp for math error

        # blank screen
        screen.fill(CALM_AZURE)
        draw_toolstrip()

        # Draw Nodes
        draw_nodes()
        draw_facts()
        draw_bonds()
        pygame.display.set_caption(window_title)


        for event in pygame.event.get():
            # Detect if window is being closed
            if event.type == pygame.QUIT:
                pygame_running = False




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

                    # check if over fact
                    for num, fact in enumerate(fact_list):
                        # check if box selected
                        if fact.box.collidepoint(event.pos):
                            changeable_fact = num
                        # check if circle selected
                        for i, corner in enumerate(fact.corners):
                            # if within radius of the circle
                            if ((event.pos[0] - corner[0]) ** 2 + (event.pos[1] - corner[1]) ** 2) <= 25:
                                if build_line == False: # Start making line
                                    build_line = True
                                    initial_corner = (fact, i)
                                else: # finish making line
                                    build_line = False
                                    terminate_corner = (fact, i)

                    # check if over toolstrip icon
                    for num, tool in enumerate(tools_list):
                        if tool.collidepoint(event.pos):
                            #if selected_tool == None:
                            selected_tool = num
                            cursor_colour = tool_choices[num][1]




                if event.button == 3: # right mouse button
                    # check if mouse over box
                    for num, node in enumerate(node_list):
                        # check if box selected
                        if node.box.collidepoint(event.pos):
                            draggable_node = node

                    # check if mouse over box
                    for num, fact in enumerate(fact_list):
                        # check if box selected
                        if fact.box.collidepoint(event.pos):
                            draggable_node = fact

                    if selected_tool != None:
                        if selected_tool == 0:
                            node_list.append(nodes.Node(event.pos[0], event.pos[1], SERAPH, "New_Node"))
                            selected_tool = None
                        if selected_tool == 1:
                            fact_list.append(nodes.Fact(event.pos[0], event.pos[1], VISION_AZURE, "New_Fact"))
                            selected_tool = None

                    if build_line == True:
                        build_line = False
                        initial_corner = None
                        terminate_corner = None




            # move active node
            if event.type == pygame.MOUSEMOTION:
                # Draw Cursor
                if selected_tool == None:
                    cursor_colour = VISION_AZURE
                if build_line:
                    cursor_colour = LINE_MAKE
                pygame.draw.circle(screen, cursor_colour, event.pos, 5)

                # Action Logic
                if draggable_node != None:
                    draggable_node.set_position(event.pos[0], event.pos[1])
                if draggable_fact != None:
                    draggable_fact.set_position(event.pos[0], event.pos[1])
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