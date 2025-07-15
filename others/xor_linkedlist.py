class Node:
    def __init__(self, data):
        self.data = data
        self.npx = 0  # XOR of addresses of previous and next nodes

class XorLinkedList:
    def __init__(self):
        self.head = None
        self._nodes = {}  # Store node objects to prevent garbage collection


    def _get_node(self, address):
        """Helper to get a node object from its simulated address (id)"""
        # In a real C/C++ implementation, you would dereference the address directly.
        # In Python, we retrieve the actual object from our stored references.
        return self._nodes.get(address)


    def insert(self, data):
        new_node = Node(data)
        self._nodes[id(new_node)] = new_node  # Store reference

        if self.head is None:
            self.head = new_node
        else:
            current_head_address = id(self.head)
            new_node.npx = current_head_address ^ 0 # new node's npx is XOR of head and NULL (0)

            # Update the previous head's npx to include the new_node
            # head->npx was previously (NULL ^ next_node_of_original_head)
            # Now, it needs to be (new_node_address ^ next_node_of_original_head)
            # next_node_of_original_head_address = self._xor(self.head.npx, 0)
            self.head.npx = id(new_node) ^ self.head.npx
            
            self.head = new_node # New node becomes the head

    def insert_at(self, index, data):
        if index == 0:
            self.insert(data)
            return

        new_node = Node(data)
        self._nodes[id(new_node)] = new_node

        prev_id = 0
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError("Index out of bounds")
            next_id = prev_id ^ current.npx
            prev_id, current = id(current), self._get_node(next_id)
        print(current.data)

        # Link new_node between prev and current
        new_node.npx = id(current) ^ prev_id

        prev_node = self._get_node(prev_id)
        if prev_node:
            prev_node.npx ^= id(current) ^ id(new_node)
        if current:
            current.npx ^= prev_id ^ id(new_node)

    def remove_at(self, index):
        prev_id = 0
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError("Index out of bounds")
            next_id = prev_id ^ current.npx
            prev_id, current = id(current), self._get_node(next_id)

        if current is None:
            raise IndexError("Index out of bounds")

        next_id = prev_id ^ current.npx
        prev_node = self._get_node(prev_id)
        next_node = self._get_node(next_id)

        if prev_node:
            prev_node.npx ^= id(current) ^ next_id
        if next_node:
            next_node.npx ^= id(current) ^ prev_id

        if current == self.head:
            self.head = next_node

        del self._nodes[id(current)]  # Let it die 😌🪦


    def print_list(self):
        current_node = self.head
        prev_node_address = 0  # Represents NULL

        print("XOR Linked List (forward traversal):")
        while current_node is not None:
            print(current_node.data, end=" -> ")
            next_node_address = prev_node_address ^ current_node.npx
            prev_node_address = id(current_node)
            current_node = self._get_node(next_node_address)
        print("None")

xor_list = XorLinkedList()
xor_list.insert(10)
xor_list.insert(20)
xor_list.insert(30)
xor_list.insert(40)
xor_list.print_list()  # Output: 40 -> 30 -> 20 -> 10 -> None

xor_list.insert_at(2, 25)   # Insert 25 at index 2
xor_list.print_list()       # Should show: 40 -> 30 -> 25 -> 20 -> 10 -> None

xor_list.remove_at(3)       # Remove element at index 3 (which is 20)
xor_list.print_list()       # Should show: 40 -> 30 -> 25 -> 10 -> None

