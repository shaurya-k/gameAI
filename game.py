import copy
import random
# shaurya kethireddy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, person):
        board = copy.deepcopy(state)
        pieces = []
        drop = self.counter(state)
        if drop:  # under 8
            for i in range(5):
                for j in range(5):
                    if board[i][j] == ' ':
                        successor = copy.deepcopy(board)
                        successor[i][j] = person
                        pieces.append(successor)
        else:  # already 8
            for i in range(5):
                for j in range(5):
                    if board[i][j] == person:

                        if (i - 1) > -1 and board[i - 1][j] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i - 1][j] = person
                            pieces.append(successor)

                        if (i + 1) < 5 and board[i + 1][j] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i + 1][j] = person
                            pieces.append(successor)

                        if (j + 1) < 5 and board[i][j + 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i][j + 1] = person
                            pieces.append(successor)

                        if (i + 1) < 5 and (j + 1) < 5 and board[i + 1][j + 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i + 1][j + 1] = person
                            pieces.append(successor)

                        if (j - 1) > -1 and board[i][j - 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i][j - 1] = person
                            pieces.append(successor)

                        if (i - 1) > -1 and (j - 1) > -1 and board[i - 1][j - 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i - 1][j - 1] = person
                            pieces.append(successor)

                        if (i + 1) < 5 and (j - 1) > -1 and board[i + 1][j - 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i + 1][j - 1] = person
                            pieces.append(successor)

                        if (i - 1) > -1 and (j + 1) < 5 and board[i - 1][j + 1] == ' ':
                            successor = copy.deepcopy(board)
                            successor[i][j] = ' '
                            successor[i - 1][j + 1] = person
                            pieces.append(successor)
        return pieces

    def heuristic_game_value(self, state):
        hval = self.game_value(state)
        if hval != 0:
            return hval
        heuristics = [hval]

        for row in state:
            for i in range(2):
                playerCount = 0
                aiCount = 0
                emptyCount = 0
                for j in range(2):
                    if row[i + j] == ' ':
                        emptyCount += 1
                    elif row[i + j] == self.my_piece:
                        playerCount += 1
                    else:
                        aiCount += 1

                if aiCount == 3 and aiCount == 0:
                    heuristics.append(-.8)
                elif playerCount == 0 and aiCount == 2:
                    heuristics.append(-.6)
                elif playerCount == aiCount:
                    heuristics.append(0)
                elif playerCount == 1 and aiCount == 0:
                    heuristics.append(.2)
                elif playerCount == 2 and aiCount == 0:
                    heuristics.append(.6)
                elif playerCount == 3 and aiCount == 0:
                    heuristics.append(.8)
                else:
                    heuristics.append(0)

        for col in range(5):
            for i in range(2):
                playerCount = 0
                aiCount = 0
                emptyCount = 0
                for j in range(2):
                    if state[i + j][col] == ' ':
                        emptyCount += 1
                    elif state[i + j][col] == self.my_piece:
                        playerCount += 1
                    else:
                        aiCount += 1

                if aiCount == 3 and aiCount == 0:
                    heuristics.append(-.8)
                elif playerCount == 0 and aiCount == 2:
                    heuristics.append(-.6)
                elif playerCount == aiCount:
                    heuristics.append(0)
                elif playerCount == 1 and aiCount == 0:
                    heuristics.append(.2)
                elif playerCount == 2 and aiCount == 0:
                    heuristics.append(.6)
                elif playerCount == 3 and aiCount == 0:
                    heuristics.append(.8)
                else:
                    heuristics.append(0)

        h_value = sum(heuristics) / len(heuristics)  # avg
        return h_value

    def counter(self, state):  # iterates through board and checks pieces
        num = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    num += 1
        if num < 8:
            return True
        return False

    def max_value(self, state, depth):
        hval = self.heuristic_game_value(state)
        if hval == 1 or depth < 1:
            return hval, state
        else:
            holder = float(-100000)
            successors = self.succ(state, self.my_piece)
            for x in successors:  # Go through each successor, find highest a value
                if self.min_val(x, depth - 1) > holder:
                    holder = self.min_val(x, depth - 1)
                    toReturn = x
        return holder, toReturn

    def min_val(self, state, depth):
        hval = self.heuristic_game_value(state)
        if hval == -1 or depth < 1:
            return hval
        else:
            holder = float(100000)
            successors = self.succ(state, self.opp)
            for x in successors:
                holder = min(holder, self.max_value(x, depth - 1)[0])
        return holder

    def make_move(self, state):
        move = []
        a, holder = self.max_value(state, 3)
        drop = self.counter(state)

        if drop:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ' and holder[i][j] == self.my_piece:
                        move.insert(0, (i, j))
                        return move

        if not drop:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == self.my_piece and holder[i][j] == ' ':
                        piece = (i, j)
                    if state[i][j] == ' ' and holder[i][j] == self.my_piece:
                        destination = (i, j)

            move.append(destination)
            move.append(piece)
            return move
        return 0  # error

    def opponent_move(self, move):

        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        """
        # horizontals
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # verticals
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        if state[0][0] != ' ' and state[0][0] == state[1][1] == state[2][2] == state[3][3]:
            return 1 if state[0][0] == self.my_piece else -1
        if state[0][1] != ' ' and state[0][1] == state[1][2] == state[2][3] == state[3][4]:
            return 1 if state[0][1] == self.my_piece else -1
        if state[1][1] != ' ' and state[1][1] == state[2][2] == state[3][3] == state[4][4]:
            return 1 if state[1][1] == self.my_piece else -1
        if state[1][0] != ' ' and state[1][0] == state[2][1] == state[3][2] == state[4][3]:
            return 1 if state[1][0] == self.my_piece else -1

        if state[0][4] != ' ' and state[0][4] == state[1][3] == state[2][2] == state[3][1]:
            return 1 if state[0][4] == self.my_piece else -1
        if state[1][3] != ' ' and state[1][3] == state[2][2] == state[3][1] == state[4][0]:
            return 1 if state[1][3] == self.my_piece else -1
        if state[0][3] != ' ' and state[0][3] == state[1][2] == state[2][1] == state[3][0]:
            return 1 if state[0][3] == self.my_piece else -1
        if state[1][4] != ' ' and state[1][4] == state[2][3] == state[3][2] == state[4][1]:
            return 1 if state[1][4] == self.my_piece else -1

        # check 3x3 square corners wins
        for i in range(1, 4):
            for j in range(1, 4):
                if state[i + 1][j] != ' ' and state[i][j] == ' ' and state[i + 1][j] == state[i][j + 1] == state[i - 1][j] == state[i][j - 1]:
                    return 1 if state[i + 1][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                player_move = player_move.upper()
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                    player_move = player_move.upper()
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                move_from = move_from.upper()
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                    move_from = move_from.upper()
                move_to = input("Move to (e.g. B3): ")
                move_to = move_to.upper()
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                    move_to = move_to.upper()
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
