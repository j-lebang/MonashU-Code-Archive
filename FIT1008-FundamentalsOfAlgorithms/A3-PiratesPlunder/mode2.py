from island import Island

from data_structures.referential_array import ArrayR
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    
    UNLESS STATED OTHERWISE, EACH LINE HAS O(1) COMPLEXITY

    Data Structures used:
    - Dictionary
    - Max Heap

    Due to complexity requirements, we need to use a data structure
    that can do add, update, retrieve, and delete in constant time.
    A data structure which can do this is a dictionary. So islands
    are stored in the dictionary with the island's name as the key
    and the island itself as the value.

    Since the pirates are perfect logicians, we want to optimise
    the choices selected by each and every pirate. In order to
    achieve this, we can store the amount of money that can be
    obtained on every island given a certain amount of crew.
    Due to complexity requirements, we need to use a data structure
    which can keep track of the maximum amount of money we can achieve
    at the current state of given amount of crews and islands. We
    can do this with a MaxHeap.

    note: island.py is modified (given comparator functions) so that it can work
          correctly within the MaxHeap
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Student-TODO: Best/Worst Case

        Complexity:
        Best Case: O(1)
        Worst Case: O(1)
        """
        self.c = n_pirates
        self.islands = {}

    def add_islands(self, islands: list[Island]):
        """
        Student-TODO: Best/Worst Case
        
        Complexity: I is the length of the `islands` list
        Best Case: O(I)
        Worst Case: O(I)
        """
        for island in islands: # O(I)
            self.islands[island.name] = island

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Student-TODO: Best/Worst Case

        Complexity: N is the length of self.islands
                    C is self.c (the number of captains participating)
        Best Case: O(N + Clog(N))
        Worst Case: O(N + Clog(N))
        """
        available_islands = ArrayR(len(self.islands)) # O(N)
        i = 0
        for island in self.islands: # O(N)
            temp = self.islands[island]
            money = temp.money + 2 * (crew - temp.marines) if crew >= temp.marines else (temp.money * crew / temp.marines)
            available_islands[i] = (money, self.islands[island])
            i += 1
        
        available_islands = MaxHeap.heapify(available_islands) # O(N)

        def attack(money, island): # O(1)
            temp, res = crew, money
            sent = min(temp, island.marines)
            # temp -= sent
            # if temp > 0:
            #     res += temp * 2
            return (res, sent)
        
        pirates = [None] * self.c # O(C)
        for i in range(self.c): # O(C)
            # print("before:\n", self.islands)
            skip = crew * 2
            raid = None
            if len(available_islands):
                money, island = available_islands.get_max() # O(log(N))
                raid = attack(money, island)
                # print(i, island, raid)
            
            if raid is None or skip > raid[0]:
                pirates[i] = (None, 0)
                if raid is not None:
                    available_islands.add((money, island))
            else:
                pirates[i] = (island, raid[1])
                island.money -= raid[1] / island.marines * island.money
                island.marines -= raid[1]

                # print(island, island.money, island.marines)
            
            # if raid is not None:
                if island.money > 0:
                    self.islands[island.name] = Island(island.name, island.money, island.marines)
                    
                    temp = self.islands[island.name]
                    r_money = temp.money + 2 * (crew - temp.marines) if crew >= temp.marines else (temp.money * crew / temp.marines)
                    available_islands.add((r_money, self.islands[island.name]))
                else:
                    del self.islands[island.name]
        
            # print("after:\n", self.islands)

        return pirates