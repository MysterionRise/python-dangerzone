from random import random, randint


class Node:

    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next_node = next_node

    def get_data(self):
        return self.value

    def get_next_node(self):
        return self.next_node

    def set_next_node(self, new_next):
        self.next_node = new_next


def generate_linked_list(size: int, prob: float) -> Node:
    head = Node(value=0)
    prev_node = head
    prev_nodes = []
    loop = False
    ind = 0
    while ind < size and not loop:
        if random() > 1.0 - prob and len(prev_nodes) > 0:
            prev_node.set_next_node(prev_nodes[randint(0, len(prev_nodes) - 1)])
            loop = True
        else:
            next_node = Node(value=ind)
            prev_node.set_next_node(next_node)
            prev_nodes.append(prev_node)
            prev_node = next_node
        ind += 1
    return head
