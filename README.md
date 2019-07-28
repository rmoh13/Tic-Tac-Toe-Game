# Tic-Tac-Toe-Game
A Tic-Tac-Toe Game in Python 3
I made a multiplayer networked version, local multiplayer version, and a version of the game where you can play against an AI that knows what it is doing or an AI that has no clue what it is doing and is just making random moves.

I implemented the AI algorithm using the minimax algorithm. See below for my personal understanding of the minimax algorithm.

# Minimax Algorithm: Motivation, Intuition, and Explanation
First, assume that each player is a perfectly rational player and plays to win (that is their incentive). Ok, now, essentially, when we're playing Chess, in our minds, we're thinking of all different combinations of different chess moves possible given we move one piece and the opponent moves another which causes us to make another decision, etc. We map out different possibility streams in our mind, and with our AI, we're speeding up that process using computational power. We essentially do build a map of all different possible games of Tic-Tac-Toe from that current moment and onwards. How do we get a computer to do this and do it in an optimized manner so that it is extremely quick? Our AI has to internally makes/compute moves from the perspective of the opponent, and we want to map out all of these possible games where we win and lose, and we want to minimize the maximum gain of our opponent, so essentially minimize the moves that benefit the opponent meaning that we also minimize our maximum loss OR if we look at the other side of the coin in which case this fact, minimax == maximin, holds true in zero-sum games (Zero-Sum Situations happen when whatever one loses, the other gains and vice versa) like Tic-Tac-Toe, we want to maximize our own minimum gain meaning that maximize whatever minimum wins we have meaning we also we maximize the opponent's minimum loss.

In this Tic-Tac-Toe AI, we'll use a maximin algorithm if the AI is 'X' and it's minimax if it's 'O', we're going to run the AI on our current position, compute all possible games starting from that current position, assign a score for each position (high scores for when we win), and then we choose the move that eventually gives us the highest/maximum score, and we run this recursively on each position we're in as the game progresses. The algorithm looks at things from the perspective of the opponent too, so it calculates all the moves in the POV of the opponent that favors them winning and looks to minimaze the score while it also calculates the moves from the POV of itself and looks to maximize the score. This whole process uses recursion or divide and conquer as a more simple and clean way of tackling the problem, where we backtrack through all possible states, and at the very top of the stack or the last stack frame is the last call to the minimax_score function and that is when we reach the terminal state and then we return respective scores for each of the three outcomes ('X' winning returns +10 because we assume the AI to be 'X', 'O' winning returns -10, and a draw returns 0), and then that score is passed up back up one step in the tree and now at that point in the tree, it collects all the scores from the leafs and choices below chooses the min (for 'O' to win) or max (for 'X' to win) score.
