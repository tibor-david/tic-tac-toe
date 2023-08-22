import curses
from .tictactoe_logic import TicTacToeLogic

_board_str = """\
     |     |     
  1  |  2  |  3  
_____|_____|_____
     |     |     
  4  |  5  |  6  
_____|_____|_____
     |     |     
  7  |  8  |  9  
     |     |     
"""


class TicTacToeCurses:
    """A class allowing you to play tic tac toe in the terminal against an algorithm."""

    def __init__(self) -> None:
        self.ttt = TicTacToeLogic()

    def _coords_to_cell(self, row, col):
        return (row * 3 + col) + 1

    def _get_available_cells(self):
        return [
            (row, col)
            for row in range(3)
            for col in range(3)
            if self.ttt.board[row][col] == "-"
        ]

    def _clear_line(self, y):
        self.stdscr.move(y, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def _init_curses(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        curses.noecho()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, -1)

    def _show_available_cells(self, exclude_cell):
        for cell in self._get_available_cells():
            if cell != exclude_cell:
                row = {0: 1, 1: 4, 2: 7}[cell[0]]
                col = {0: 2, 1: 8, 2: 14}[cell[1]]

                self.stdscr.addstr(
                    row,
                    col,
                    str(self._coords_to_cell(cell[0], cell[1])),
                    curses.color_pair(4),
                )
        self.stdscr.refresh()

    def _print_board(self):
        actual_board = _board_str
        for row in range(3):
            for col in range(3):
                if self.ttt.board[row][col] != "-":
                    actual_board = actual_board.replace(
                        str(self._coords_to_cell(row, col)),
                        self.ttt.board[row][col].upper(),
                    )
        self.stdscr.addstr(0, 0, actual_board)
        self.stdscr.refresh()

    def _set_cell_cursor(self, row, col, state, char):
        cell = char.upper() if char != "-" else str(self._coords_to_cell(row, col))
        available_cells = self._get_available_cells()

        _row = {0: 1, 1: 4, 2: 7}[row]
        _col = {0: 2, 1: 8, 2: 14}[col]

        if state == "select":
            if (row, col) in available_cells:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(3)

            # Top of the cell
            self.stdscr.addstr(_row - 1, _col - 2, " " * 5, color)

            # Middle of the cell
            self.stdscr.addstr(_row, _col - 2, "  ", color)
            self.stdscr.addstr(_row, _col, cell, color)
            self.stdscr.addstr(_row, _col + 1, "  ", color)

            # Bottom of the cell
            if _row < 7:
                self.stdscr.addstr(_row + 1, _col - 2, "_" * 5, color)
            else:
                self.stdscr.addstr(_row + 1, _col - 2, " " * 5, color)

        elif state == "deselect":
            # Top of the cell
            self.stdscr.addstr(_row - 1, _col - 2, " " * 5)

            # Middle of the cell
            self.stdscr.addstr(_row, _col - 2, " " * 2)
            self.stdscr.addstr(_row, _col, cell)
            self.stdscr.addstr(_row, _col + 1, " " * 2)

            # Bottom of the cell
            if _row < 7:
                self.stdscr.addstr(_row + 1, _col - 2, "_" * 5)
            else:
                self.stdscr.addstr(_row + 1, _col - 2, " " * 5)

        self.stdscr.refresh()

    def _ask_for_cell(self):
        keys_enter = [curses.KEY_ENTER, 10, 13]

        row = 0
        col = 0
        char = ""

        prvs_row = row
        prvs_col = col
        prvs_chr = self.ttt.board[row][col]

        while True:
            char = self.ttt.board[row][col]

            self._set_cell_cursor(row, col, "select", char)
            self._show_available_cells((row, col))

            key = self.stdscr.getch()
            if key == curses.KEY_UP and row > 0:
                row -= 1

            elif key == curses.KEY_DOWN and row < 2:
                row += 1

            elif key == curses.KEY_LEFT and col > 0:
                col -= 1

            elif key == curses.KEY_RIGHT and col < 2:
                col += 1

            elif key in keys_enter:
                if char == "-":
                    self._clear_line(10)
                    return row, col
                else:
                    self._clear_line(10)
                    curses.napms(50)

                    self.stdscr.addstr(
                        10,
                        0,
                        "The cell is already used, please choose another one.",
                        curses.color_pair(1),
                    )

            self._set_cell_cursor(prvs_row, prvs_col, "deselect", prvs_chr)

            prvs_row = row
            prvs_col = col
            prvs_chr = self.ttt.board[row][col]

    def play(self):
        """Start the game in the terminal."""
        turn = 1
        self._init_curses()
        self._print_board()

        while True:
            self._print_board()
            if turn % 2 == 0:
                if turn == 2 and self.ttt.board[1][1] == "-":
                    self.ttt.play_cell(1, 1, "x")
                else:
                    row, col = self.ttt.make_best_move()
                    self.ttt.play_cell(row, col, "x")
            else:
                row, col = self._ask_for_cell()
                self.ttt.play_cell(row, col, "o")

            # Check if there are a win or a tie
            if self.ttt.check_win() or self.ttt.check_tie():
                self._print_board()

                if self.ttt.check_win():
                    winner = "The bot has" if turn % 2 == 0 else "You"
                    self.stdscr.addstr(10, 0, f"{winner} won.")

                elif self.ttt.check_tie():
                    self.stdscr.addstr(10, 0, "There was a tie.")

                self.stdscr.refresh()

                # Write the tictactoe board in the stdout
                stdscr_content = []
                for row in range(11):
                    stdscr_content.append(self.stdscr.instr(row, 0).decode())

                self.ttt.reset_board()
                self.stdscr.clear()
                curses.endwin()
                print("".join(stdscr_content))

                break
            turn += 1
