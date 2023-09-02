import copy
from typing import Literal


class TicTacToeLogic:
    def __init__(self):
        self._board = [["-" for _ in range(3)] for _ in range(3)]

    @property
    def board(self):
        return copy.deepcopy(self._board)

    def play_cell(self, row: int, col: int, player: Literal["x", "o"]) -> None:
        self._board[row][col] = player

    def check_win(self) -> bool:
        """
        Check if the game has been won by any player.

        Returns:
            bool: True if there is a winner, False otherwise.
        """

        # Check if there are a win in the rows
        for row in range(3):
            if (
                self._board[row][0] == self._board[row][1] == self._board[row][2]
                and self._board[row][0] != "-"
            ):
                self.winner = self._board[row][0]
                return True

        # Check if there are a win in the columns
        for col in range(3):
            if (
                self._board[0][col] == self._board[1][col] == self._board[2][col]
                and self._board[0][col] != "-"
            ):
                self.winner = self._board[0][col]
                return True

        # Check if there are a win in the left diagonal
        if (
            self._board[0][0] == self._board[1][1] == self._board[2][2]
            and self._board[0][0] != "-"
        ):
            self.winner = self._board[0][0]
            return True

        # Check if there are a win in the right diagonal
        if (
            self._board[0][2] == self._board[1][1] == self._board[2][0]
            and self._board[0][2] != "-"
        ):
            self.winner = self._board[0][2]
            return True
        return False

    def check_tie(self) -> bool:
        """
        Check if the game is a tie.

        Returns:
            bool: True if the game is a tie, False otherwise.
        """

        for row in range(0, 3):
            for col in range(0, 3):
                if self._board[col][row] == "-":
                    return False
        return not self.check_win()

    def reset_board(self):
        """
        Reset the game board to start a new game.
        """
        self._board = [["-" for _ in range(3)] for _ in range(3)]

    def minimax(self, robot_turn: bool, depth: int = 0) -> int:
        """
        Perform the minimax algorithm to evaluate the best move for the robot player.

        Args:
            robot_turn (bool): True if it's the robot's turn, False if it's the player's turn.
            depth (int, optional): The depth of the minimax search. Defaults to 0.

        Returns:
            int: The score of the evaluated move.
        """

        score = []
        if self.check_tie():
            return 0
        elif self.check_win():
            if robot_turn:
                if self.winner == "x":
                    return 10 - depth
                else:
                    return -10 + depth

        for row in range(3):
            for col in range(3):
                if self._board[row][col] == "-":
                    if robot_turn:
                        self._board[row][col] = "x"
                    else:
                        self._board[row][col] = "o"
                    score.append(self.minimax(not robot_turn, depth=depth + 1))
                    self._board[row][col] = "-"
        if robot_turn:
            return max(score)
        else:
            return min(score)

    def make_best_move(self) -> tuple:
        """
        Find and return the best move for the robot player using the minimax algorithm.

        Returns:
            tuple: The row and column indices of the best move.
        """

        best_move = tuple()
        best_score = -float("inf")

        for row in range(3):
            for col in range(3):
                if self._board[row][col] == "-":
                    self._board[row][col] = "x"
                    score = self.minimax(False)
                    self._board[row][col] = "-"
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move
