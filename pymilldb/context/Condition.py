class Condition(object):

    def __init__(self, left, right, op, right_is_parameter):
        self.left = left
        self.right = right
        self.op = op
        self.rip = right_is_parameter
