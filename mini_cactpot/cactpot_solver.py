"""
Mini-Cactpot Solver
Zachary McCullough
2021-05-16
zam.mccullough@gmail.com
"""

#########
# Imports
#########

import random
import typing as t
import itertools


#########
# Classes
#########


class Board:
    sums = {
        6: 10000,
        7: 36,
        8: 720,
        9: 360,
        10: 80,
        11: 252,
        12: 108,
        13: 72,
        14: 54,
        15: 180,
        16: 72,
        17: 180,
        18: 119,
        19: 36,
        20: 306,
        21: 1080,
        22: 144,
        23: 1800,
        24: 3600,
    }

    lines = {
        0: lambda x: x[0:3],  # top across
        1: lambda x: x[3:6],  # middle across
        2: lambda x: x[6:9],  # bottom across
        3: lambda x: x[0:7:3],  # left down
        4: lambda x: x[1:8:3],  # middle down
        5: lambda x: x[2:9:3],  # right down
        6: lambda x: x[0:9:4],  # diag l-r down
        7: lambda x: x[2:7:2],  # diag r-l down
    }

    intersections = {
        0: {0, 3, 6},
        1: {0, 4},
        2: {0, 5, 7},
        3: {1, 3},
        4: {1, 4, 6, 7},
        5: {1, 5},
        6: {2, 3, 7},
        7: {2, 4},
        8: {2, 5, 6},
    }

    def __init__(self):
        self.arr = ["*"] * 9
        self.used = set()

    def __repr__(self):
        out = ""
        for i in range(3):
            out += "\t".join(str(x) for x in self.arr[i * 3 : i * 3 + 3]) + "\n"
        return out

    def __str__(self):
        return self.__repr__()

    def reveal(self, x, y, num):
        self.arr[3 * y + x] = num
        self.used.add(num)

    @staticmethod
    def _sum(arr) -> t.Tuple[int, int]:
        """
        returns the row_sum and number of still hidden squares
        :param arr: board data struct
        :return: tuple of row_sum, # of stars
        """
        stars = 0
        total = 0
        for n in arr:
            if n == "*":
                stars += 1
            else:
                total += n
        return total, stars

    def get_line(self, index):
        return self.lines[index](self.arr)

    @staticmethod
    def _calculate_possible_sums(
        arr: t.Iterable[int], given: t.Optional[t.Iterable[int]] = None
    ) -> t.List[t.Set[int]]:
        """
        Given an input of used numbers, from the remaining ones calculate what possible sums exist. Use given
        to say one or two numbers must be used.
        :param arr: list of ints that are already used and unavailable
        :param given: list of ints (len 1 or 2)
        :return: List of each possible line generated
        """
        given_set = set() if given is None else set(given)
        given_length = len(given_set)

        arr_set = set(arr)
        if given is not None and len(arr_set.intersection(given_set)) != given_length:
            raise ValueError(
                "If a number is given, then it must be already used as well."
            )
        if given_length == 3:
            return [set(given)]

        allowed_nums = set(range(1, 10)) - set(arr)

        # iterate over
        base_combinations = itertools.combinations(
            allowed_nums - given_set, 3 - given_length
        )
        result = (
            [set(x).union(given_set) for x in base_combinations]
            if given is not None
            else [set(x) for x in base_combinations]
        )
        if len(result) == 0:
            raise ValueError("Maybe you messed up?")
        return result

    def get_possible_rows_for_line(self, line: int) -> t.List[t.Set[int]]:
        """
        Calculates every possible row for a line. Given is numbers already there, self.used is kept up to date with
        self.reveal, then calls calculate_possible_sums to do the heavy lifting
        :param line: line number
        :return: list of possible rows, each row being a set of ints. Each row consists of unique nums anyways so this
        works out great.
        """
        nums = self.get_line(line)
        given = set(nums) - set("*")
        possible_lines = self._calculate_possible_sums(self.used, given)
        return possible_lines

    def expected_line_value(self, line: int) -> float:
        """
        Calculates the expected line value by finding all possible lines, get the row_sum, then lookup what value that
        is, then calculate average score.
        :param line: the line number to check
        :return: the expected value
        """
        possible_lines = self.get_possible_rows_for_line(line)
        return sum(self.sums[sum(x)] for x in possible_lines) / len(possible_lines)

    def highest_expected_value_left(self) -> t.Tuple[int, float]:
        """
        Very similar to highest_expected_value_line, calculates highest expected but skips revealed ones
        :return: Tuple of highest non-revealed lin num and then score associated with it
        """
        line_num = -1
        max_score = -1
        for i in range(len(self.lines)):
            if "*" not in self.lines[i](self.arr):
                continue
            score = self.expected_line_value(i)
            if score > max_score:
                line_num = i
        return line_num, max_score

    def highest_expected_value_line(self) -> t.Tuple[int, float]:
        """
        Calculates expected value of each line, returning line and value
        :return: Tuple of highest line num and the score associated with it
        """
        line_num = -1
        max_score = -1
        for i in range(len(self.lines)):
            score = self.expected_line_value(i)
            if score > max_score:
                line_num = i
                max_score = score
        return line_num, max_score

    def lines_intersection(self, i: int) -> t.Iterable[int]:
        """
        Reveals which lines go through this square
        :param i: which square to check
        :return: set of lines
        """
        return self.intersections[i]

    def expected_value_through_square(self, i) -> float:
        """
        Given a square, calculates expected value of each line crossing through it and averages possibilities
        :param i: the square
        :return: expected mgp value
        """

        # first get the lines we care about
        lines = self.lines_intersection(i)
        possibilities = []
        for line in lines:
            possibilities.extend(self.get_possible_rows_for_line(line))

        return sum(self.sums[sum(x)] for x in possibilities) / len(possibilities)

    def optimal_click(self):
        """
        Determines the optimal square to reveal by calculating for each square the averaged expected value of each
        line that crosses that square, skipping revealed squares (since you can't reveal a revealed square obviously)
        For tiebreaker in case multiple lines have same probability (e.g. first), it picks the square that has the most
        lines that cross it which will be middle for first guess. No idea if this is truly optimal but it seems
        reasonable, future work could be improving.
        :return: None
        """
        square = -1
        max_score = -1
        tie_breaker = -1
        for i in range(9):
            if self.arr[i] != "*":
                continue
            score = self.expected_value_through_square(i)
            if score > max_score or (
                score == max_score and len(self.intersections[i]) > tie_breaker
            ):
                max_score = score
                square = i
                tie_breaker = len(self.intersections[i])
        return square


class Interact:
    """
    This is a helper class that will drive a game of mini-cactpot, creating a true board and interacting with the
    Board class
    """

    def __init__(self, board=None):
        if board is not None:
            self.true_board = board
        else:
            self.true_board = random.sample(range(1, 10), 9)
        self.board = Board()
        self.final_result = None

    @staticmethod
    def _coord(x: int) -> t.Tuple[int, int]:
        return x % 3, x // 3

    def play_game(self) -> None:
        """
        Plays a single game, consuming this object, updating final_result with the score
        :return: None
        """
        for j in range(4):
            self.take_turn()
        optimal_line, _ = self.board.highest_expected_value_line()
        self.final_result = self.choose_line(optimal_line)

    def choose_line(self, line: int) -> int:
        """
        Chooses the line and gets the score and reveals everything
        :param line: the line number
        :return: the score value result
        """
        self.board.arr = self.true_board
        score = self.board.sums[
            sum(self.board.get_line(line))
        ]  # sums the optimal line, then returns score
        return score

    def take_turn(self) -> None:
        """
        Take an individual turn
        :return: None
        """
        square_to_click = self.board.optimal_click()
        x_coord, y_coord = self._coord(square_to_click)
        self.board.reveal(x_coord, y_coord, self.true_board[square_to_click])


def main():
    pass


if __name__ == "__main__":
    main()
