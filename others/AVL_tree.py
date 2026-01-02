class Node:
    def __init__(self, key):
        self.key: int = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = 1
    
    def right_rotate(self) -> "Node":
        if self.left is None:
            return self
        x = self.left
        self.left = x.right
        x.right = self
        self.height = self.get_height()
        x.height = x.get_height()
        return x
    
    def left_rotate(self) -> "Node":
        if self.right is None:
            return self
        x = self.right
        self.right = x.left
        x.left = self
        self.height = self.get_height()
        x.height = x.get_height()
        return x

    def get_balance(self) -> int:
        lh, rh = 0, 0
        if self.left:
            lh = self.left.height
        if self.right:
            rh = self.right.height
        return lh - rh
    
    def get_height(self) -> int:
        lh, rh = 0, 0
        if self.left:
            lh = self.left.height
        if self.right:
            rh = self.right.height
        return max(lh, rh) + 1

    def insert(self, key) -> "Node":
        if key < self.key:
            if self.left is None:
                self.left = Node(key)
            else:
                self.left = self.left.insert(key)
        else:
            if self.right is None:
                self.right = Node(key)
            else:
                self.right = self.right.insert(key)

        self.height = self.get_height()

        # balance
        balance = self.get_balance()
        if balance > 1: # left is too big
            if self.left and key < self.left.key: # the insertion happened on left of left
                return self.right_rotate()
            elif self.left: # inserted on right of left
                self.left = self.left.left_rotate()
                return self.right_rotate()
        elif balance < -1: # right is too big
            if self.right and key > self.right.key:
                return self.left_rotate()
            elif self.right:
                self.right= self.right.right_rotate()
                return self.left_rotate()
        
        return self

    def in_order(self, height=0):
        if self.left:
            self.left.in_order()
        
        if self.right:
            self.right.in_order()

    def display(self, prefix=''):
        """Prints the tree in a pretty format"""
        if self.left:
            self.left.display(prefix + '  ')
            print(prefix + ' /')
        print(prefix + str(self.key))
        if self.right:
            print(prefix + ' \\')
            self.right.display(prefix + '  ')
        if prefix == "": print('-'*20)

a = Node(20)
a.display()
a = a.insert(15)
a.display()
a = a.insert(5)
a.display()
a = a.insert(40)
a.display()
a = a.insert(50)
a.display()
a = a.insert(18)
a.display()
