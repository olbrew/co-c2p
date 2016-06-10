class CallStack:

    def __init__(self):
        self.address_stack = []
        self.address_stack.append(5)

    def getAddress(self, space=1):
        assert space >= 0
        address = self.address_stack[-1]
        # TODO maybe this will be needed for recursion
        #self.address_stack[-1] = address + space
        return address

    def getNestingDepth(self):
        return len(self.address_stack) - 1

    def incrementDepth(self):
        self.address_stack.append(5)

    def decrementDepth(self):
        self.address_stack.pop()
