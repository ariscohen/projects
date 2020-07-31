class SudokuNum:
    def __init__(self, val, locked):
        self.val = val
        self.locked = locked


class SudokuBoard:
    def __init__(self):
        self.board = [[SudokuNum(0, False) for i in range(9)] for j in range(9)]
        self.helpArr = [0 for i in range(10)]  # helps check if each 9 part has more than 1 digit
        self.curIndex = 0
        self.find_starting_index()

    # should return -1 if wrong, 0 if good in progress, and 1 if done

    def setup_board(self):  # no error checking
        while True:
            row = int(input('Enter row (1-9), or -1 to stop: '))
            if row == -1:
                self.print_board()
                return
            col = int(input('Enter col (1-9: '))
            num = int(input('Enter number: '))
            self.board[row-1][col-1].locked = True
            self.board[row-1][col-1].val = num

    # in case 1st number locked, find closest place to start guessing
    @staticmethod
    def index_to_rc(index):
        row = index // 9
        col = index % 9
        return [row, col]

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(str(self.board[i][j].val) + " ", end=" ")
            print()

    # accounts for locked squares
    def step_forward(self):
        found_next = False
        orig = self.curIndex

        while not found_next:
            self.curIndex += 1
            rc = SudokuBoard.index_to_rc(self.curIndex)
            if not self.board[rc[0]][rc[1]].locked:
                found_next = True
            # check if reached the last square. if yes, could not have solved
            # since we would have checked the entire board already.
            else:
                if self.curIndex == 80:
                    self.curIndex = orig
                    found_next = True

    # when tried all options, set current square to 0 and go back
    def step_back(self):
        rc = SudokuBoard.index_to_rc(self.curIndex)
        self.board[rc[0]][rc[1]].val = 0
        self.curIndex -= 1
        found = False

        if self.curIndex == -1: # program ended
            return

        while not found:
            rc = SudokuBoard.index_to_rc(self.curIndex)
            if self.board[rc[0]][rc[1]].locked:
                self.curIndex -= 1
            else:
                found = True

    def find_starting_index(self):
        valid_start = False
        while not valid_start:
            rc = SudokuBoard.index_to_rc(self.curIndex)
            if self.board[rc[0]][rc[1]].locked:
                self.curIndex += 1
            else:
                valid_start = True

    def reset_help(self):
        for i in range(10):
            self.helpArr[i] = 0

    def check_help(self, show):
        zero_index = True
        can_complete = False
        valid = True

        for i in self.helpArr:
            if zero_index:
                if i == 0:
                    can_complete = True
                zero_index = False
            else:
                if i > 1:
                    valid = False
                    break
        if show:
            for q in range(10):
                print(self.helpArr[q], end=" ")
        self.reset_help()

        if can_complete and valid:
            return 1
        elif (not can_complete) and valid:
            return 0
        else:
            return -1

    def check_rows(self):
        ovr_status = 1
        for row in self.board:
            for i in row:
                self.helpArr[i.val] = self.helpArr[i.val] + 1
            cur_status = self.check_help(False)

            if cur_status < ovr_status:
                ovr_status = cur_status
            if ovr_status == -1:
                return -1
        return ovr_status

    def check_cols(self):
        ovr_status = 1
        for i in range(9):
            for row in self.board:
                self.helpArr[row[i].val] = self.helpArr[row[i].val] + 1
            cur_status = self.check_help(False)

            if cur_status < ovr_status:
                ovr_status = cur_status
            if ovr_status == -1:
                return -1
        return ovr_status

    def check_quads(self):
        ovr_status = 1
        for i in range(9):
            start_col = (i % 3)*3
            start_row = (i//3)*3
            # iterate through each 3x3 board starting from its upper left corner
            for j in range(3):
                for k in range(3):
                    val = self.board[start_row + j][start_col + k].val
                    self.helpArr[val] = self.helpArr[val] + 1
            cur_status = self.check_help(False)

            if cur_status < ovr_status:
                ovr_status = cur_status
            if ovr_status == -1:
                return -1
        return ovr_status

    def check_board(self):
        status = self.check_rows()
        if status == -1:
            return -1
        status = min(status, self.check_cols())
        if status == -1:
            return -1
        status = min(status, self.check_quads())
        return status

    def solve(self):
        while self.curIndex >= 0:
            rc = SudokuBoard.index_to_rc(self.curIndex)
            if self.board[rc[0]][rc[1]].val == 9:  # backtrack
                # if self.curIndex == 80:
                    # print('Incorrect board incoming!')
                    # self.print_board()
                # print('stepping back')
                # self.print_board()
                self.step_back()
                continue
            else:
                self.board[rc[0]][rc[1]].val += 1

            status = self.check_board()
            if status == 1:  # found the solution
                print('Found it!')
                self.print_board()
                return True
            elif status == 0:  # move on, may backtrack
                # print('stepping forward')
                # self.print_board()
                self.step_forward()
            else:
                # self.print_board()
                continue
            # if status is -1 will keep incrementing current square


sud = SudokuBoard()
sud.setup_board()
sud.solve()

