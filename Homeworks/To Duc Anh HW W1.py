try:
    import numpy as np  # calculation
    import tkinter as tk  # interface
except ImportError as e:
    print(e)


class Player:
    def __init__(self, name, number):
        self._name = name
        self._number = number

    def get_number(self):
        return self._number

    def __str__(self):
        return self._name.title()


class Caro:
    def check_win(self, game_board, turn):
        raise NotImplementedError('Will be implemented in child class')

    def display_board(self, game_board):
        raise NotImplementedError('Will be implemented in child class')

    def play(self):
        raise NotImplementedError('Will be implemented in child class')


class Tictactoe(Caro):
    def __init__(self):
        super().__init__()
        player_1_name = input('Enter player 1 name: ')
        player_2_name = input('Enter player 2 name: ')
        self.player_1 = Player(name=player_1_name, number=1)
        self.player_2 = Player(name=player_2_name, number=-1)

    def check_win(self, game_board, turn):
        if self._check_row(game_board) or self._check_col(game_board) or self._check_diag_negative(
                game_board) or self._check_diag_positive(game_board) == 1:
            return 1  # gamemode 1: player 1 won
        elif self._check_row(game_board) or self._check_col(game_board) or self._check_diag_negative(
                game_board) or self._check_diag_positive(game_board) == -1:
            return -1  # gamemode -1: player -1 won
        elif turn == 9:
            return 2  # gamemode 2: draw
        else:
            return 0  # gamemode 0: keep going

    def _check_row(self, game_board):
        tol = np.sum(game_board, axis=1, dtype='int8')
        for i in tol:
            if i == 3:
                return 1
            elif i == -3:
                return -1
            else:
                return 0

    def _check_col(self, game_board):
        tol = np.sum(game_board, axis=0, dtype='int8')
        for i in tol:
            if i == 3:
                return 1
            elif i == -3:
                return -1
            else:
                return 0

    def _check_diag_positive(self, game_board):
        diag_positive = np.sum(np.diagonal(game_board))
        if diag_positive == 3:
            return 1
        elif diag_positive == -3:
            return -1
        else:
            return 0

    def _check_diag_negative(self, game_board):
        diag_negative = np.sum(np.fliplr(game_board).diagonal())
        if diag_negative == 3:
            return 1
        elif diag_negative == -3:
            return -1
        else:
            return 0

    def display_board(self, game_board):
        length = len(game_board[0])
        print('   ', end='')
        for i in range(length - 1):
            print(i, end=' ')
        print(length - 1)
        for i in range(len(game_board)):
            print(i, game_board[i])

    def _reset(self):
        return np.zeros(shape=(3, 3), dtype='int')

    def _flip_player(self, player):
        if player.get_number() == 1:
            player = self.player_2
        elif player.get_number() == -1:
            player = self.player_1
        return player

    def _take_turn(self, gameboard, turn, player):
        authenticate = False
        while authenticate is False:
            try:
                i = int(input('enter row :'))
                j = int(input('enter col :'))
                if gameboard[i][j] == 0:
                    gameboard[i][j] = player.get_number()
                    authenticate = True
                else:
                    print('space occupied, choose another one')
            except ValueError:
                print('Invalid data, enter again')
                authenticate = False

        turn += 1
        return gameboard, turn

    def play(self):
        game_board = np.zeros(shape=(3, 3), dtype='int')  # initialize the gameboard
        # data = np.array([[0, 1, 1], [0, 1, 0], [1, 0, 0]], dtype='int8')
        print('GAME STARTED PALS!')
        self.display_board(game_board)
        turn = 0
        player = self.player_1
        while turn != 9:
            print(f"{player}'s turn")
            game_board, turn = self._take_turn(game_board, turn, player)
            player = self._flip_player(player)
            self.display_board(game_board)
            if self.check_win(game_board, turn) == 1:
                print(f'{self._flip_player(player)} won')
                stat = input('do you want to play again?(y/n)')
                if stat == 'y':
                    turn = 0
                    game_board = self._reset()
                    print('Game Started')
                elif stat == 'n':
                    print('Game Ended')
                    break
                else:
                    print('Invalid input, ending game....')
                    break

            elif self.check_win(game_board, turn) == -1:
                print(f'{self._flip_player(player)} won')
                stat = input('do you want to play again?(y/n)')
                if stat == 'y':
                    turn = 0
                    game_board = self._reset()
                    print('Game Started')
                elif stat == 'n':
                    print('Game Ended')
                    break
                else:
                    print('Invalid input, ending game....')
                    break

            elif self.check_win(game_board, turn) == 2:
                print('game draw')
                stat = input('do you want to play again?(y/n)')
                if stat == 'y':
                    turn = 0
                    game_board = self._reset()
                    print('Game Started')
                elif stat == 'n':
                    print('Game Ended')
                    break
                else:
                    print('Invalid input, ending game....')
                    break


if __name__ == '__main__':
    Tictactoe().play()
