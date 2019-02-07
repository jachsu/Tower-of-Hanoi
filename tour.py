"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    n = model.get_number_of_cheeses()
    for move in move_of_four(n, 0, 1, 2, 3):
        if animate:
            model.move(move[0], move[1])
            print(model)
            time.sleep(delay_btw_moves)
        else:
            model.move(move[0], move[1])


def m(n):
    """
    return the minimum number of moves needed
    to move n cheeses from stool 0 to stool 3.

    @type n: int
    @rtype: int
    """
    l = []
    if n <= 2:
        return 2**n-1
    else:
        for i in range(1, n):
            l.append(2*m(n - i) + 2**i - 1)
        return min(l)


def get_i(n):
    """
    return the special number i so that m(n) is the minimum.
    precondition: n >= 2
    @type n: int
    @rtype: int
    """
    l = []
    for i in range(1, n):
        l.append(2*m(n - i) + 2**i - 1)
        if min(l) == m(n):
            return i


def move_of_four(n, source, inter1, inter2, dest):
    """
    return a list of moves which takes the least steps
    to move n cheeses from source to dest through inter1 and inter2.
    @type n: int
    @type source: int
    @type inter1: int
    @type inter2: int
    @type dest: int
    @rtype: list
    """
    l = []
    if n == 1:
        l.append([source, dest])
    elif n == 2:
        l.append([source, inter1])
        l.append([source, dest])
        l.append([inter1, dest])
    elif n == 3:
        if l == []:  # 2 inters
            l.append([source, inter1])
            l.append([source, inter2])
            l.append([source, dest])
            l.append([inter2, dest])
            l.append([inter1, dest])
        else:
            l += move_of_three(n, source, inter2, dest)
    if n > 3:
        # move n-i cheeses from src to  inter1
        l += move_of_four(n - get_i(n), source, dest, inter2, inter1)
        # move i cheeses from src to dest, stool 1 occupied
        l += move_of_three(get_i(n), source, inter2, dest)
        # move n-i cheeses from inter 1 to dest
        l += move_of_four(n - get_i(n), inter1, source, inter2, dest)
    return l


# credit to prof Danny Heap
def move_of_three(n, source, intermediate, destination):
    """Move n cheeses from source to destination in the model of three stools

    @param int n:
    @param int source:
    @param int intermediate:
    @param int destination:
    @rtype: None
    """
    l = []
    if n > 1:
        l += move_of_three(n - 1, source, destination, intermediate)
        l += move_of_three(1, source, intermediate, destination)
        l += move_of_three(n - 1, intermediate, source, destination)
    else:
        l.append([source, destination])
    return l


if __name__ == '__main__':
    num_cheeses = 8
    delay_between_moves = 0.5
    console_animate = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)

    print(four_stools.number_of_moves())
    # Leave files below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    import python_ta
    python_ta.check_all(config="tour_pyta.txt")
