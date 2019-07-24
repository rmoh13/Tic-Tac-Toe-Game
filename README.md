# Tic-Tac-Toe-Game
A Tic-Tac-Toe Game in Python 3
I made a multiplayer networked version, local multiplayer version, and a version of the game where you can play against an AI that knows what it is doing or an AI that has no clue what it is doing and is just making random moves.

I implemented the AI algorithm using the minimax algorithm. See below for my personal understanding of the minimax algorithm.

# Minimax Algorithm Motivation, Intuition, and Explanation
Essentially, when we're playing Chess, in our minds, we're thinking of all different combinations of different chess moves possible given we move one piece and the opponent moves another which causes us to make another decision, etc. We map out different possibility streams in our mind, and with our AI, we're speeding up that process using computational power. We essentially do build a map of all different possible games of Tic-Tac-Toe from that current moment and onwards.
