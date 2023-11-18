from island import Island

from data_structures.bst import *

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117

    UNLESS STATED OTHERWISE, EACH LINE HAS O(1) COMPLEXITY

    Data Structures used:
    - Binary Search Tree

    To achieve the maximum amount of money we can get with a given number of crew,
    we can keep choosing islands with the highest ratio of money to marines. Due
    to complexity requirements, we could use a binary search tree to store the
    islands. This way it fulfills the complexity requirements for accessing
    islands and updating islands.

    note: island.py is modified (given comparator functions) so that it can work
          correctly within the BinarySearchTree
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Student-TODO: Best/Worst Case

        Complexity: N is the length of the `islands` list
        Best Case: O(Nlog(N))
        Worst Case: O(Nlog(N))
        """
        self.crew = crew
        self.bst = BinarySearchTree()
        for island in islands: # O(N)
            ratio = island.money / island.marines
            self.bst[ratio] = island # O(log(N))

    def get(self, crew: int = -1):
        """
        Function to calculate select_islands and 
        select_islands_from_crew_numbers.
        The logic is similar so I abstracted logic
        into one single function.

        Complexity: N is the size of the BST (number of islands that exist)
        Best Case: O(1) When the root has no right child and marines in the
                   root node's island, is more than the crew
        Worst Case: O(N) When we are able to visit each and every island
                    present in the BST in order to get the most money
        """
        if crew == -1:
            crew = self.crew

        total = 0
        result = []
        def traverse(current: TreeNode): 
            nonlocal crew, total

            if current is None:
                return
            
            traverse(current.right)
            if crew > 0:
                temp = min(crew, current.item.marines)
                crew -= temp

                ratio = current.item.money / current.item.marines
                total += ratio * temp
                result.append((current.item, temp))
            traverse(current.left)

        traverse(self.bst.root)
        return (result, total)

    
    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Student-TODO: Best/Worst Case

        Complexity: N is the size of the BST (number of islands that exist)
        Best Case: O(1) When the root has no right child and marines in the
                   root node's island, is more than the crew
        Worst Case: O(N) When we are able to visit each and every island
                    present in the BST in order to get the most money
        """
        return self.get()[0]
    
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Student-TODO: Best/Worst Case

        Complexity: N is the size of the BST (number of islands that exist)
                    C is the size of `crew_numbers` list
        Best Case: O(C) When every crew number is less than the number of
                   marines in the root node's island and there is no right
                   child for the root node
        Worst Case: O(C * N) When for each crew number, we go through the
                    entire tree
        """
        result = []
        for crew_number in crew_numbers: # O(C)
            result.append(self.get(crew_number)[1]) # O(N)
        return result

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Student-TODO: Best/Worst Case

        Complexity: N is the size of the BST (number of islands that exist)
        Best Case: O(1) When the searched node is the root and has only one child
        Worst Case: O(log(N)) When the searched node is a leaf [We assumed the
                    depth of the tree to be bounded by O(log(N))]
        """
        ratio = island.money / island.marines
        name = self.bst[ratio].name # O(1) / O(log(N))
        del self.bst[ratio] # O(1) / O(log(N))

        new_ratio = new_money / new_marines
        self.bst[new_ratio] = Island(name, new_money, new_marines) # O(log(N))
