# Tic-Tac-Toe-Game
A Tic-Tac-Toe Game in Python 3
I made a multiplayer networked version, local multiplayer version, and a version of the game where you can play against an AI that knows what it is doing or an AI that has no clue what it is doing and is just making random moves.

I implemented the AI algorithm using the minimax algorithm. See below for my personal understanding of the minimax algorithm.

# Minimax/Maximin (In Zero-Sum Situations where whatever one loses, the other gains and vice versa) Algorithm: Motivation, Intuition, and Explanation
Essentially, when we're playing Chess, in our minds, we're thinking of all different combinations of different chess moves possible given we move one piece and the opponent moves another which causes us to make another decision, etc. We map out different possibility streams in our mind, and with our AI, we're speeding up that process using computational power. We essentially do build a map of all different possible games of Tic-Tac-Toe from that current moment and onwards. How do we get a computer to do this and do it in an optimized manner so that it is extremely quick? Our AI has to internally makes/compute moves from the perspective of the opponent, and we want to map out all of these possible games where we win and lose, and we want to minimize the maximum gain of our opponent, so essentially minimize the moves that benefit the opponent meaning that we also minimize our maximum loss OR if we look at the other side of the coin in which case this fact, minimax == maximin, holds true in zero-sum games like Tic-Tac-Toe, we want to maximize our own minimum gain meaning that maximize whatever minimum wins we have meaning we also we maximize the opponent's minimum loss.

In the maximin algorithm, we're going to run 
