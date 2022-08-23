"""
AVL tree implementation obtained from: https://gist.github.com/Twoody/de8d079842e0dd20cf20d870c73168af
"""

#import random, math

outputdebug = False 

def debug(msg):
    if outputdebug:
        print (msg)

class Node():
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None 

class AVLTree():
    def __init__(self, *args):
        self.node = None 
        self.height = -1  
        self.balance = 0; 
        
        if len(args) == 1: 
            for i in args[0]: 
                self.insert(i)
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 
    
    def insert(self, key):
        tree = self.node
        
        newnode = Node(key)
        
        if tree == None:
            self.node = newnode 
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
            debug("Inserted key [" + str(key) + "]")
        
        elif key < tree.key: 
            self.node.left.insert(key)
            
        elif key > tree.key: 
            self.node.right.insert(key)
        
        else: 
            debug("Key [" + str(key) + "] already in tree.")

        self.update_heights()
        self.update_balances()
        self.rebalance()
        
    def rebalance(self):
        ''' 
        Rebalance a particular (sub)tree
        ''' 
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()
 
    def rrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' right') 
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T
    
    def lrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 

    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 

    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 

    def delete(self, key):
        # debug("Trying to delete at node: " + str(self.node.key))
        if self.node != None: 
            if self.node.key == key: 
                debug("Deleting ... " + str(key))  
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None # leaves can be killed at will 
                # if only one subtree, take that 
                elif self.node.left.node == None: 
                    self.node = self.node.right.node
                elif self.node.right.node == None: 
                    self.node = self.node.left.node
                
                # worst-case: both children present. Find logical successor
                else:  
                    replacement = self.logical_successor(self.node)
                    if replacement != None: # sanity check 
                        debug("Found replacement for " + str(key) + " -> " + str(replacement.key))  
                        self.node.key = replacement.key 
                        
                        # replaced. Now delete the key from right child 
                        self.node.right.delete(replacement.key)
                    
                self.rebalance()
                return  
            elif key < self.node.key: 
                self.node.left.delete(key)  
            elif key > self.node.key: 
                self.node.right.delete(key)
                        
            self.rebalance()
        else: 
            return 

    def logical_predecessor(self, node):
        ''' 
        Find the biggest valued node in LEFT child
        ''' 
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 

    def logical_successor(self, node):
        ''' 
        Find the smallese valued node in RIGHT child
        ''' 
        node = node.right.node  
        if node != None: # just a sanity check  
            
            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
    
        return inlist 

    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''
        self.update_heights()  # Must update heights before balances
        self.update_balances()
        if(self.node != None): 
            print ('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", 'L' if self.is_leaf() else ' '    )
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

    def uncorrupted_merge(self, other, corrupted):
        """ Removes all corrupted keys from the corrupted AVL Tree and merges the corrupted AVL Tree to
            the main AVL Tree, self. Merge algorithm obtained and modified from
            https://stackoverflow.com/questions/2037212/concatenating-merging-joining-two-avl-trees
        :param other: AVL Tree that is corrupted
        :param corrupted: List of corrupted keys
        :best time complexity: O(k log M) where N = Number of keys in self, M = Number of keys in other,
                               and k = Number of keys in corrupted when all keys in other are corrupted
        :worst time complexity: O(k log M + log N) otherwise
        """
        # Delete Corrupted Keys
        for key in corrupted:
            other.delete(key)

        # If self is bigger than other
        if self.height > other.height:
            # Get max node from other
            N = other.get_max_node()

            # Delete from other if exists and merge to left of self
            if N is not None:
                other.delete(N.key)
                self.uncorrupted_merge_aux_left(other, N)

        # If other is bigger than self
        else:
            # Swap self and other
            self.node, other.node = other.node, self.node
            self.height, other.height = other.height, self.height
            self.balance, other.balance = other.balance, self.balance

            # Get min node from other
            N = other.get_min_node()

            # Delete from other if exists and merge to right of self
            if N is not None:
                other.delete(N.key)
                self.uncorrupted_merge_aux_right(other, N)

    def uncorrupted_merge_aux_left(self, other, N):
        """ Method to merge an AVL tree that is both smaller in size and keys than self while
            maintaining balance. Obtained and modified from
            https://stackoverflow.com/questions/2037212/concatenating-merging-joining-two-avl-trees
        :param other: AVL Tree that is smaller in size and where all keys are smaller than keys in self
        :param N: The node with the biggest key in other
        :time complexity: O(log N) where N = Number of keys in self
        """
        # Base Case
        if self.height <= other.height + 1:
            # Set N as new root node, other as left child, previous root as right child
            N.left = other
            N.right = AVLTree()
            N.right.node = self.node
            self.node = N

        # Go left until we reach base case
        else:
            self.node.left.uncorrupted_merge_aux_left(other, N)

        # Re-balance as we go up
        self.update_heights()
        self.update_balances()
        self.rebalance()

    def uncorrupted_merge_aux_right(self, other, N):
        """ Method to merge an AVL tree that is smaller in size and larger in keys than self while
            maintaining balance. Obtained and modified from
            https://stackoverflow.com/questions/2037212/concatenating-merging-joining-two-avl-trees
        :param other: AVL Tree that is smaller in size and where all keys are larger than keys in self
        :param N: The node with the smallest key in other
        :time complexity: O(log N) where N = Number of keys in self
        """
        # Base Case
        if self.height <= other.height + 1:
            # Set N as new root node, previous root as left child, other as right child
            N.left = AVLTree()
            N.left.node = self.node
            N.right = other
            self.node = N

        # Go right until we reach base case
        else:
            self.node.right.uncorrupted_merge_aux_right(other, N)

        # Re-balance as we go up
        self.update_heights()
        self.update_balances()
        self.rebalance()

    def get_max_node(self):
        """ Gets the node with the biggest key in an AVL Tree
        :return: Node with biggest key
        :time complexity: O(log N) where N = Number of keys in self
        """
        # Initialise Current
        node = self.node

        # AVL Tree is empty, return None
        if node is None:
            return node

        # Go right until we cannot go right
        while node.right is not None:
            if node.right.node is None:
                return node
            else:
                node = node.right.node

    def get_min_node(self):
        """ Gets the node with the smallest key in an AVL Tree
        :return: Node with smallest key
        :time complexity: O(log N) where N = Number of keys in self
        """
        # Initialise Current
        node = self.node

        # AVL Tree is empty, return None
        if node is None:
            return node

        # Go left until we cannot go left
        while node.left is not None:
            if node.left.node is None:
                return node
            else:
                node = node.left.node


# Usage example
if __name__ == "__main__":
    myself = AVLTree([6969696969])
    other = AVLTree([420, 0, -9, 3454, 421, 232, 12121, 9])
    corrupted = [420]
    myself.uncorrupted_merge(other, corrupted)
    myself.display()
    # for key in corrupted:
    #     other.delete(key)
    # other.display()
