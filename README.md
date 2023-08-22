# Tic Tac Toe Library


## Overview

This library provides a command-line interface for playing Tic Tac Toe against a minimax algorithm. You can engage in a classic game of Tic Tac Toe directly from your terminal.

Furthermore, this library's flexibility allows you to integrate it into your projects, such as developing a graphical user interface or other applications by using the `TicTacToeLogic` class.

## Installation

### There are two methods for installing the library:


1. **Build the Library**

   This method is more intricate. If you're new to Python, consider the second installation method instead.

   1. Ensure that you have the necessary dependencies installed on your machine: wheel, setuptools, and build. On Debian/Ubuntu-based Linux systems, you can use your package manager: `apt install python3-build python3-setuptools python3-wheel`. On Windows, you can utilize pip directly: `py -m pip install --user --upgrade build pip setuptools wheel`.

   2. Execute the command `pyproject-build` at the root of the repository.

   3. This will generate a "dist" folder and a "tictactoe.egg-info" folder. Disregard the "tictactoe.egg-info" file and navigate into the "dist" folder.

   4. Inside the "dist" folder, you'll find two files: "tictactoe-x.y.z-py3-none-any.whl" and "tictactoe-x.y.z.tar.gz". If you intend to install the library on your machine or within a virtual environment, select the *.whl file. Copy the file's path and use the command `pip install <path to the file>/tictactoe-x.y.z-py3-none-any.whl` for installation.

2. **Directly use pip**

   You can directly run the command: `pip install git+https://github.com/tibor-david/tic-tac-toe` without the need to clone the repository.

## How to Play

### Initiating the Game

You can start playing in two ways:

1. **Importing the Library**:

   Create a Python file and include the following lines:

   ```python
   from titactoe import TicTacToecCurses

   ttt = TicTacToe()
   ttt.play()
   ```

2. **Running the Library as a Module**:

   From your shell, execute the following command:

   ```shell
   $ python3 -m tictactoe
   ```

### Starting the game

To play, simply move using the arrows on your keyboard to select your square. Once your choice is made, press Enter to confirm your move. The minimax algorithm will then make its move, and the game will continue. The available cells are displayed in green. 
