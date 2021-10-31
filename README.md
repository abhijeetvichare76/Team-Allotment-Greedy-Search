# Team-Allotment-Greedy-Search
This problem is part of the assignment of course CS-551 (Elements of Artificial Intelligence) taught by Prof. David Crandall. This code was created in collaboration with Sreekar Chigurupati and Raksha Rank.
## Problem statement
We are required to allot students to teams. based on mutual preference and non-preference. Appropriate costs for allocations are specified.

## Equivalence with SRP
This is a modified versions of a well-known problem called the "Stable Roomates Problem"(SRP) with some modifications. Stable roomates problem is the problem of finding a stable matching for an even sized set. The modification required to reduce current problem to SRP is to let any number of roomates <= 3 to a room.

It has been showed that switching the number of beds from 2 to 3 makes the problem NP-complete.

Reference:
> K. Iwama, S. Miyazaki, and K. Okamoto, "Stable roommates problem with triple rooms." Proc. 10th KOREA-JAPAN Joint Workshop on Algorithms and Computation (WAAC 2007), pp. 105–112, 2007

## Approach

Given the NP-completeness of the problem, there will be no polynomial time efficient solution. Heuristic or greedy approaches look like a good fit.

### First attempt
We started by attempting a greedy approach.
  
**Search space**: All sets of sets from power set of students

**Start state**: Null set

**Succesor function**: set with an element added to current state with the added element being a minimum cost valid merger of two states from powerset of students not alloted to a team yet

**Goal state**: A set containing partitions of the student set

**Cost function**: Cost of a group is evaluation cost + size cost + likes cost + dislikes cost

This approach failed because the sets with single student are the costly at each step.

Next we tried to penalize shorter sets. This didnt consistently work out as longer sets with more students who dont prefer each other may increase the cost function and cant be represented in the penalty.

***We dropped the naive greedy approach***

### Implemented approach

Defining a heuristic for the problem appears to be infeasible. The search tree for even even increase in number of students makes complete traversal intractable. 
We have started with all singleton sets of students and merged sets to generate successors


A reduction of the search space is needed. We have chosen to limit the branching factor at each level. At each exansion of the fringe, only best N elements are added and the rest of successors are discarded.

Also, this approach sometimes outputs a lot of sets with two students, as they have lower immediate cost. When two sets of size two are formed, they cant be merged further as the resulting set will have a length > 3. To overcome this limitation which may prevent efiicient merges that may reduce the overall cost. We have included to method to check for partitions of the set of 4 elements which reduce overall cost.


**Search space**: All possible partitions of students set

**Start state**: Set of sets with individual students

**Successor function**: Set of sets derived from current state with two elements merged validly

**Cost function**: sum of all costs of elements in state

This approach scales well and the branching factor can be tweaked to optimize runtime. We have set the branching factor to be 5. This is a sort of  **bounded best-first search** approach.
