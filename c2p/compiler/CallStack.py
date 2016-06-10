class CallStack:

    def __init__(self):
        self.address_stack = []
        self.address_stack.append(5)

    def getAddress(self):
        return self.address_stack[-1]

    def incrementAddress(self, space):
        assert space >= 0
        self.address_stack[-1] += space

    def getNestingDepth(self):
        return len(self.address_stack) - 1

    def incrementDepth(self):
        self.address_stack.append(5)

    def decrementDepth(self):
        self.address_stack.pop()
