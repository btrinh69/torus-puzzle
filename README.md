# torus-puzzle
This program solve the Torus 8-Puzzle. Illustration of Torus 8-Puzzle:

|1 2 3| =>  |1 2 3|

|4 5 6| =>  |4 5 6|

|7 0 8| =>  |7 8 0|
            (Goal)

The game is initialized by putting numbers from 1-8 into the 9 positions board (0 represent the empty space) and the player can slide the number to the adjacent empty space. The goal is to reach the state where numbers are in ascending order (showed above).
In this version, the empty space is adjacent to a number if it is above, below, on the left, and right. The number can also be wrap around vertically and horizontally to the opposite side. Illustration:

|1 2 3| => |1 0 3|

|4 5 6| => |4 5 6|

|7 0 8| => |7 2 8|

(Number 2 is wrapped from the first row to the bottom row)

In the program, the state is illustrated by the flattened 1-D array. For example, the state:

|1 2 3| is represented as [1,2,3,4,5,6,7,0,8]

|4 5 6|

|7 0 8|

The program makes use of A* search algorithm:

	Goal state: [1,2,3,4,5,6,7,8,0]
    
	Heuristic: the number of numbers which are not in its right position. For example, the state [1,2,3,4,5,6,7,0,8] has the heuristic value of 1 as number 8 is not in its right position
