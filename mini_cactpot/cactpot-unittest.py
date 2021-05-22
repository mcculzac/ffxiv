"""
Mini-Cactpot Solver: unittest
Zachary McCullough
2021-05-16
zam.mccullough@gmail.com
"""

#########
# Imports
#########

import unittest
from mini_cactpot import cactpot_solver


#######
# Class
#######


class MyTestCase(unittest.TestCase):
    def test_calculate_possible_sums(self):
        b = cactpot_solver.Board()
        used = [1, 2, 3, 4, 5, 6]
        self.assertEqual([{7, 8, 9}], b._calculate_possible_sums(used))
        self.assertEqual(
            [{6, 8, 9}, {7, 8, 9}, {6, 7, 8}, {6, 7, 9}],
            b._calculate_possible_sums(used[:-1]),
        )
        self.assertEqual(
            [{1, 2, 8}, {1, 2, 9}, {1, 2, 7}], b._calculate_possible_sums(used, [1, 2])
        )
        self.assertEqual(84, len(b._calculate_possible_sums([])))

    def test_expected_line_val(self):
        b = cactpot_solver.Board()
        for i in range(8):
            self.assertAlmostEqual(360.3452380, b.expected_line_value(i), 2)

    def test_lines(self):
        b = cactpot_solver.Board()
        b.arr = [3, 6, 1, 9, 4, 8, 5, 2, 7]
        self.assertEqual([3, 6, 1], b.get_line(0))
        self.assertEqual([9, 4, 8], b.get_line(1))
        self.assertEqual([5, 2, 7], b.get_line(2))
        self.assertEqual([3, 9, 5], b.get_line(3))
        self.assertEqual([6, 4, 2], b.get_line(4))
        self.assertEqual([1, 8, 7], b.get_line(5))
        self.assertEqual([3, 4, 7], b.get_line(6))
        self.assertEqual([1, 4, 5], b.get_line(7))

    def test_reveal(self):
        b = cactpot_solver.Board()
        b.reveal(0, 0, 3)
        self.assertEqual([3, "*", "*", "*", "*", "*", "*", "*", "*"], b.arr)
        b.reveal(1, 1, 4)
        self.assertEqual([3, "*", "*", "*", 4, "*", "*", "*", "*"], b.arr)
        b.reveal(2, 2, 7)
        self.assertEqual([3, "*", "*", "*", 4, "*", "*", "*", 7], b.arr)
        b.reveal(0, 2, 5)
        self.assertEqual([3, "*", "*", "*", 4, "*", 5, "*", 7], b.arr)
        b.reveal(2, 0, 1)
        self.assertEqual([3, "*", 1, "*", 4, "*", 5, "*", 7], b.arr)
        b.reveal(0, 1, 9)
        self.assertEqual([3, "*", 1, 9, 4, "*", 5, "*", 7], b.arr)
        b.reveal(1, 0, 6)
        self.assertEqual([3, 6, 1, 9, 4, "*", 5, "*", 7], b.arr)
        b.reveal(2, 1, 8)
        self.assertEqual([3, 6, 1, 9, 4, 8, 5, "*", 7], b.arr)
        b.reveal(1, 2, 2)
        self.assertEqual([3, 6, 1, 9, 4, 8, 5, 2, 7], b.arr)

    def test_highest_expected_value_left(self):
        b = cactpot_solver.Board()
        b.arr = [3, 6, 1, 9, 4, 8, 5, 2, 7]
        b.used = b.arr
        self.assertEqual(80, b.expected_line_value(0))
        self.assertEqual(1080, b.expected_line_value(1))
        self.assertEqual(54, b.expected_line_value(2))
        self.assertEqual(180, b.expected_line_value(3))
        self.assertEqual(108, b.expected_line_value(4))
        self.assertEqual(72, b.expected_line_value(5))
        self.assertEqual(54, b.expected_line_value(6))
        self.assertEqual(80, b.expected_line_value(7))

    # def test_highest_expected_value_line_2(self):
    #     """
    #     this test is not valid!!!
    #     :return:
    #     """
    #     b = cactpot_solver.Board()
    #     b.arr = [3, 6, 1,
    #              9, 4, 8,
    #              5, 2, 7]
    #     b.used = [3, 6, 1,
    #               9, 4, 8,
    #               5, 2, 7]
    #     reset_arr = [3, 6, 1,
    #                  9, 4, 8,
    #                  5, 2, 7]
    #     reset_used = [3, 6, 1,
    #                   9, 4, 8,
    #                   5, 2, 7]
    #     values = [1, 1, 5] * 3
    #     for i, k in enumerate(b.arr):
    #         b.used.pop(i)
    #         b.used.pop(i)
    #         b.arr[i] = '*'
    #         b.arr[i+1] = '*'
    #         self.assertEqual(values[i], b.highest_expected_value_line())
    #         b.used = copy.deepcopy(reset_arr)
    #         b.arr = copy.deepcopy(reset_used)

    def test_optimal_1(self):
        b = cactpot_solver.Board()
        self.assertEqual(4, b.optimal_click())

    def test_optimal_2(self):
        b = cactpot_solver.Board()
        b.arr = [3, 6, 1, "*", 4, 8, 5, "*", 7]
        b.used = [3, 6, 1, 4, 8, 5, 7]
        self.assertEqual(3, b.optimal_click())
        b.arr = [3, 6, "*", "*", 4, 8, 5, "*", 7]
        b.used = [3, 6, 4, 8, 5, 7]
        self.assertEqual(2, b.optimal_click())
        b.arr = ["*", 6, "*", "*", 4, 8, 5, "*", 7]
        b.used = [6, 4, 8, 5, 7]
        self.assertEqual(2, b.optimal_click())

    # def test_stress_test(self):
    #     coord = lambda x: (x%3, x//3)
    #     result = []
    #     for i in range(10000):
    #         b = cactpot_solver.Board()
    #         hidden_cactpot = random.sample(range(1, 10), 9)
    #         for j in range(3):
    #             square_to_click = b.optimal_click()
    #             x_coord, y_coord = coord(square_to_click)
    #             b.reveal(x_coord, y_coord, hidden_cactpot[square_to_click])
    #         result.append(b.highest_expected_value_line()[1])
    #     print('Over 10000 avg:', sum(result) / len(result))

    def test_average(self):
        max_iters = 30000
        summed_scores = 0
        for i in range(max_iters):
            if i % 1000 == 0 and i > 0:
                print(i, "iteration. Score:", summed_scores, "Avg:", summed_scores / i)
            game = cactpot_solver.Interact()
            game.play_game()
            summed_scores += game.final_result

        print("Average Line Score: ", summed_scores / max_iters)


if __name__ == "__main__":
    unittest.main()
