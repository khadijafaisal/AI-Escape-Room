class State:
    def __init__(self, name, a1, k1, k2):
        self.name = name
        self.a1 = a1
        self.k1 = k1
        self.k2 = k2
        self.children = []
        self.parents = []
        self.traversed = False
        self.move_up = None
        self.move_down = None
        self.move_left = None
        self.move_right = None

    def set(self, agent):
        agent.state = self
        agent.cell = self.a1

    def set_children(self, children):
        for child in children:
            self.children.append(child)
            child.parents.append(self)

    def get_name(self):
        return self.name

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents

    def get_traversed_parents(self):
        return [parent for parent in self.parents if parent.traversed]

    def get_traversed(self):
        return self.traversed

    def set_traversed(self, state):
        self.traversed = state

    def up(self, state):
        self.move_up = state

    def down(self, state):
        self.move_down = state

    def left(self, state):
        self.move_left = state

    def right(self, state):
        self.move_right = state
        
    