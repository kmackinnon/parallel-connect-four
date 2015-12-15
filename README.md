# parallel-connect-four

We would like to investigate how well a parallelized AI agent can play the game Connect Four compared to a sequential AI with the same task.

To run the AI, navigate to the folder that contains the files and enter the following command:

python connect4.py


Once the game is launched, several options are displayed. Select one to play the game you wish to play.

To change the depth or time limits of the parallel or sequential AIs, simply open either the minimaxAIParallel.py or minimaxAiSequential.py files and edit the maxTime and/or maxDepth global variables at the top of the file.

The program will automatically determine the number of CPUs your computer has available and will use as many as possible. If you wish to manually choose how many cores to use follow these steps. Open the minimaxAiParallel.py file, add a new variable to the top of the max_value_first() function like this: "numCPU = ?" where "?" is the integer number of CPUs you would like to use.
