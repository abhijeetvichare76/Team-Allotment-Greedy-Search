
#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Sreekar srchig@iu.edu
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
from itertools import chain, combinations

import pickle
import copy
import math
import random
import heapq


per_team_cost = 5
wrong_size_cost = 2
not_assigned_cost = 0.05 * 60
assigned_dislike_cost = 10


def parse_input(input_file):
    data = {}
    with open(input_file, 'r') as file:
        for line in file:
            input_line = line.split()
            name = input_line[0]
            likes = input_line[1].split('-')
            size = len(likes)
            while 'xxx' in likes: likes.remove('xxx')
            while 'zzz' in likes: likes.remove('zzz')

            dislikes = input_line[2].split(',')
            if dislikes == ['_']:
                dislikes = []
            data[name] = (size, likes, dislikes)
    return data

def cost(group, data):
    result = 0
    if group:
        result += per_team_cost
    for student in group:
        preference = data[student]
        if len(group) != preference[0]:
            result += wrong_size_cost
        for like in preference[1]:
            if not like in group:
                result += not_assigned_cost
        for dislike in preference[2]:
            if dislike in group:
                result += assigned_dislike_cost
    return result


def cost_total(groups, data):
    result = 0
    for group in groups:
        result += cost(group, data)
    return result

def merge_cost_diff(g1, g2):
    return cost(g1+g2) - cost(g1) - cost(g2)

def succ(groups):
    result = []
    #print(groups)
    # l of t of l
    possible_merges = list(chain.from_iterable(combinations(groups, r) for r in range(2,3)))
    #print(possible_merges)
    for two_tuple in possible_merges:
        groups_new = copy.deepcopy(groups)
        #print(two_tuple[1])
        tuple_length= len(two_tuple)
        if (len(list(chain.from_iterable(two_tuple)))) > 3:
            if(len(two_tuple[0]) == 2 and len(two_tuple[1]) == 2):
                set_4 = two_tuple[0]+two_tuple[1]
                combos_3_of4 = list(combinations(set_4, 3))
                for firstelem in combos_3_of4:
                    groups_new = copy.deepcopy(groups)
                    groups_new.remove(two_tuple[0])
                    groups_new.remove(two_tuple[1])
                    secondelem = list(set(set_4) - set(firstelem))
                    groups_new.append(list(firstelem))
                    groups_new.append(list(secondelem))
                    #print(groups_new)
                    #print(type(groups_new))
                    result.append(groups_new)
                    del groups_new
            continue
        for t in two_tuple:
            groups_new.remove(t)
        #groups_new.remove(two_tuple[0])
        #groups_new.remove(two_tuple[1])
        groups_new.append(list(chain.from_iterable(two_tuple)))
        #print(type(groups_new))
        result.append(groups_new)
        del groups_new
    
    #print(result)
    return result

def hyphenated_groups(groups):
    result = []
    for group in groups:
        group_str = ''
        for person in group:
            group_str += person
            group_str += '-'
        result.append(group_str[:-1])
    return result

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    data = parse_input(input_file)
    students = list(data.keys())
    min_cost = math.inf
    branching_factor = 5

    while True:
        #random.shuffle(students)
        fringe = []
        group_set = []
        for student in students:
            group_set.append([student])
        fringe.append((cost_total(group_set,data),group_set))
        #print(fringe)
        i=0
        while fringe:
            new_elem = heapq.heappop(fringe)
            new_state = new_elem[1]
            new_cost = new_elem[0]
            #print(new_state)
            #print(new_state)
            # for j in new_state:
            #     #print(j)
            #     new_cost += cost(j,data)
            #print("new state", new_state)
            current_succ = succ(new_state)
            sorted(current_succ, key=lambda x: cost_total(x,data))
            #current_succ.sort(key=lambda x: cost(x,data))
            for elem in current_succ[:branching_factor]:
                #print(elem)
                heapq.heappush(fringe,(cost_total(elem, data),elem))
            if new_cost < min_cost:
                min_cost = new_cost
                yield({"assigned-groups": hyphenated_groups(new_state), "total-cost": min_cost})
        branching_factor += 1
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
