import pygame
import random

node_ids = []
bond_ids = []
fact_ids = []

# TODO: add bond slots to nodes
# TODO: Add bond table to pandas, nodes x nodes and bonds within


def gen_node_id():
    global node_ids
    node_id = "N_0"
    while node_id == "N_0":
        id = random.randint(0,255)
        builder = "N_" + str(id)
        # make sure it doesnt already exist
        if builder not in node_ids:
            node_id = builder
            node_ids.append(node_id)

    return node_id


def gen_fact_id():
    global fact_ids
    fact_id = "F_0"
    while fact_id == "F_0":
        id = random.randint(0,255)
        builder = "F_" + str(id)
        # make sure it doesnt already exist
        if builder not in fact_ids:
            fact_id = builder
            fact_ids.append(fact_id)

    return fact_id


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


def gen_source_id():
    global fact_ids
    fact_id = "F_0"
    while fact_id == "F_0":
        id = random.randint(0,255)
        builder = "F_" + str(id)
        # make sure it doesnt already exist
        if builder not in fact_ids:
            fact_id = builder
            fact_ids.append(fact_id)

    return fact_id


def relink_object_from_id():
    pass

class Bond:
    def __init__(self, node_1, node_2, corner_1, corner_2):
        self.node_1 = node_1
        self.node_2 = node_2
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
    def __init__(self, x, y, colour, text):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour

        self.width = 100
        self.height = 50
        self.bonds = []
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.id = gen_node_id()

        self.corners = [(self.x,self.y), (self.x+self.width,self.y), (self.x, self.y+(self.height/2)),
                        (self.x+self.width, self.y+(self.height/2)), (self.x, self.y+self.height), (self.x+self.width, self.y+self.height)]

        self.active = False

        self.bonds = [None, None, None, None, None, None]


    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box.topleft = (x, y)
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]

    def set_text(self, text):
        self.text = text

    def data_out(self):
        # All data from node formatted for saving
        data = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'colour': self.colour,
            'text': self.text,
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
        self.text = data['text']
        self.bonds = data['bonds']




class Fact:
    def __init__(self, x, y, colour, title):
        self.x = x
        self.y = y
        self.title = title
        self.text = " "
        self.colour = colour

        self.width = 150
        self.height = 150
        self.bonds = []
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.id = gen_fact_id()

        self.corners = [(self.x,self.y), (self.x+self.width,self.y), (self.x, self.y+(self.height/2)),
                        (self.x+self.width, self.y+(self.height/2)), (self.x, self.y+self.height), (self.x+self.width, self.y+self.height)]

        self.active = False

        self.bonds = [None, None, None, None, None, None]


    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box.topleft = (x, y)
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]

    def set_text(self, text):
        self.text = text

    def data_out(self):
        # All data from node formatted for saving
        data = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'title': self.title,
            'text': self.text,
            'width': self.width,
            'height': self.height,
            'colour': self.colour,
            'bonds': self.bonds
        }

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.title = data['title']
        self.text = data['text']
        self.width = data['width']
        self.height = data['height']
        self.colour = data['colour']
        self.bonds = data['bonds']




class Source:
    def __init__(self, x, y, colour, text):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour

        self.width = 150
        self.height = 150
        self.bonds = []
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.id = gen_source_id()

        self.corners = [(self.x,self.y), (self.x+self.width,self.y), (self.x, self.y+(self.height/2)),
                        (self.x+self.width, self.y+(self.height/2)), (self.x, self.y+self.height), (self.x+self.width, self.y+self.height)]

        self.active = False

        self.bonds = [None, None, None, None, None, None]


    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box.topleft = (x, y)
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + (self.height / 2)),
                        (self.x + self.width, self.y + (self.height / 2)), (self.x, self.y + self.height),
                        (self.x + self.width, self.y + self.height)]

    def set_text(self, text):
        self.text = text

    def data_out(self):
        # All data from node formatted for saving
        data = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'title': self.title,
            'text': self.text,
            'width': self.width,
            'height': self.height,
            'colour': self.colour,
            'bonds': self.bonds
        }

        return data

    def data_in(self, data):
        # All data from node formatted for loading
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.title = data['title']
        self.text = data['text']
        self.width = data['width']
        self.height = data['height']
        self.colour = data['colour']
        self.bonds = data['bonds']



