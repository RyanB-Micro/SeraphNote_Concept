import pygame
import random

node_ids = []
bond_ids = []
fact_ids = []


def gen_node_id(preface):
    global node_ids
    node_id = preface
    while node_id == preface:
        id = random.randint(0,255)
        builder = preface + str(id)
        # make sure it doesnt already exist
        if builder not in node_ids:
            node_id = builder
            node_ids.append(node_id)

    return node_id


def gen_bond_id():
    global bond_ids
    bond_id = "B_0"
    while bond_id == "B_0":
        id = random.randint(0,255)
        builder = "B_" + str(id)
        # make sure it doesnt already exist
        if builder not in node_ids:
            bond_id = builder
            bond_ids.append(bond_id)

    return bond_id



class Bond:
    def __init__(self, node_1, node_2, corner_1, corner_2):
        self.node_1 = node_1
        self.node_2 = node_2
        self.node_1_id = node_1.id
        self.node_2_id = node_2.id
        self.corner_1 = corner_1
        self.corner_2 = corner_2
        self.x = 0
        self.y = 0
        self.term_x = 0
        self.term_y = 0
        self.id = gen_bond_id()
        self.text = "X is a Y"
        self.id_box = pygame.Rect(0, 0, 35, 15)

    def update_position(self):
        self.x = self.node_1.corners[self.corner_1][0]
        self.y = self.node_1.corners[self.corner_1][1]
        self.term_x = self.node_2.corners[self.corner_2][0]
        self.term_y = self.node_2.corners[self.corner_2][1]
        self.id_box.center = (
            ((self.x + self.term_x) / 2),
            ((self.y + self.term_y) / 2)
        )

    def set_text(self, text):
        self.text = text

    def refresh_connections(self, nodes_in, facts_in):
        for node in nodes_in:
            if node.id == self.node_1_id:
                self.node_1 = node
            if node.id == self.node_2_id:
                self.node_2 = node

        for fact in facts_in:
            if fact.id == self.node_1_id:
                self.node_1 = fact
            if fact.id == self.node_2_id:
                self.node_2 = fact


    def data_out(self):
        # All data from node formatted for saving
        data = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'node_1': self.node_1,
            'node_2': self.node_2,
            'text': self.text,
            'corner_1': self.corner_1,
            'corner_2': self.corner_2
        }

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.node_1 = data['node_1']
        self.node_2 = data['node_2']
        self.text = data['text']
        self.corner_1 = data['corner_1']
        self.corner_2 = data['corner_2']



class Node:
    def __init__(self, x, y, colour, title):
        self.x = x
        self.y = y
        self.title = title
        self.colour = colour

        self.width = 100
        self.height = 50
        self.bonds = []
        # self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.box = None
        self.collapse_switch = None
        self.corners = None
        self.preface = "N_"
        self.id = gen_node_id(self.preface)

        # self.corners = [(self.x,self.y), (self.x+self.width,self.y), (self.x, self.y+(self.height/2)),
        #                 (self.x+self.width, self.y+(self.height/2)), (self.x, self.y+self.height), (self.x+self.width, self.y+self.height)]

        self.active = False

        self.collapsed = False
        self.standard_height = 50
        self.collapsed_height = 50

        self.bonds = [None, None, None, None, None, None]
        self.calculate_box()
        self.calculate_corners()

    def calculate_box(self):
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collapse_switch = pygame.Rect(self.x+(self.width-15), self.y+(self.height-15), 15, 15)

    def calculate_corners(self):
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]

    def switch_size(self):
        if self.collapsed:
            self.unfold()
        else:
            self.collapse()

    def collapse(self):
        # Set collapse to true
        self.collapsed = True
        self.height = self.collapsed_height
        self.calculate_box()
        self.calculate_corners()

    def unfold(self):
        # Set collapse to true
        self.collapsed = False
        self.height = self.standard_height
        self.calculate_box()
        self.calculate_corners()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box.topleft = (x, y)
        self.collapse_switch.topleft = (self.x+(self.width-15), self.y+(self.height-15))


        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]


    def set_title(self, title):
        self.title = title

    def data_out(self):
        # All data from node formatted for saving
        data = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'colour': self.colour,
            'title': self.title,
            'bonds': self.bonds
        }

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.width = data['width']
        self.height = data['height']
        self.colour = data['colour']
        self.title = data['title']
        self.bonds = data['bonds']


class Fact(Node):
    def __init__(self, x, y, colour, title):
        super().__init__(x, y, colour, title)
        self.width = 150
        self.height = 150
        self.preface = "F_"
        self.text = ""
        self.id = gen_node_id(self.preface)

        # self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
        #                 (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
        #                 (self.x + self.width, self.y + self.height)]

        self.standard_height = 150
        self.calculate_box()
        self.calculate_corners()
        #self.collapse()

    def set_text(self, text):
        self.text = text

    def data_out(self):
        # All data from node formatted for saving
        data = super().data_out()
        data['text'] = self.text

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        super().data_in(data)
        self.text = data['text']



class Quote(Node):
    def __init__(self, x, y, colour, title):
        super().__init__(x, y, colour, title)
        self.width = 150
        self.height = 150
        self.preface = "Q_"
        self.text = ""
        self.id = gen_node_id(self.preface)
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]


    def set_text(self, text):
        self.text = text

    def data_out(self):
        # All data from node formatted for saving
        data = super().data_out()
        data['text'] = self.text

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        super().data_in(data)
        self.text = data['text']



class Source(Node):
    def __init__(self, x, y, colour, title):
        super().__init__(x, y, colour, title)
        self.width = 150
        self.height = 100
        self.preface = "S_"
        self.section = ""
        self.chapter = ""
        self.id = gen_node_id(self.preface)
        #self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
        #                 (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
        #                 (self.x + self.width, self.y + self.height)]

        self.standard_height = 150
        self.calculate_box()
        self.calculate_corners()


    def set_text(self, section, chapter):
        self.section = section
        self.chapter = chapter

    def data_out(self):
        # All data from node formatted for saving
        data = super().data_out()
        data['section'] = self.section
        data['chapter'] = self.chapter

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        super().data_in(data)
        self.section = data['section']
        self.chapter = data['chapter']





