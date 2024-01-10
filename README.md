# Gobblet-AI-Player
This repository contains an implementation of the classic board game Gobblet with an AI opponent that utilizes the Min-Max and Alpha-Beta Pruning algorithms. The AI is designed to provide challenging gameplay at easy, medium, and hard difficulty levels.

## Game Overview
Gobblet is a two-player abstract strategy game where players attempt to line up four of their own gobblets in a row. The game is played on a 4x4 board, and players can place their gobblets or move existing ones to achieve their goal.

## Features
### Modes: there is 3 modes of playing, Human vs Human, Human vs Computer, Computer vs Computer.
### Interactive Gameplay
Play Computer against the Computer opponent at different difficulty levels.
Easy, Medium, Hard Levels: Choose the level of difficulty that suits your skill level.
Random Moves: are done at easy level.
Alpha-Beta Pruning: The AI opponent at medium and hard levels incorporates Alpha-Beta Pruning to enhance efficiency.
Scalable Architecture: Designed for easy integration and expansion for future improvements.

## GUI
GUI of Gobblet Board during a Game. 

![Screenshot 2024-01-10 215152](https://github.com/ShoroukHegazy15/Gobblet-AI-Player/assets/105671159/b34f27b7-1c2e-41a0-a547-be3cc88909e9)

## Difficulty Levels
### Easy
The AI opponent at the easy level uses the random moves to make decisions. It explores the game tree up to a certain depth to find the best move.

### Medium
The AI opponent at the medium level incorporates Alpha-Beta Pruning for more efficient decision-making. This allows for deeper exploration of the game tree compared to the easy level.

### Hard
At the hard level, the AI opponent further optimizes performance with Alpha-Beta Pruning. It aims to provide a more challenging and competitive experience by exploring the game tree even deeper.

### Enjoy the game!
