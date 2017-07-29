import unittest as test
import random

from app.util.search import nearest_neighbor, lin_nearest_neighbor


class SearchingTest(test.TestCase):
    @staticmethod
    def rand_sorted(magnitude=1, size=100):
        return sorted((random.random() * magnitude for i in range(size)))

    def test_bin_nn_random(self):
        values = self.rand_sorted(magnitude=1000)
        ind = nearest_neighbor(500.0, values)
        abs_ind_err = abs(500.0 - values[ind])
        if ind > 0:
            self.assertTrue(abs_ind_err < abs(500 - values[ind - 1]),
                            "{0} is closer to 500 than {1}".format(values[ind - 1], values[ind]))
        if ind < len(values) - 1:
            self.assertTrue(abs_ind_err < abs(500 - values[ind + 1]),
                            "{0} is closer to 500 than {1}".format(values[ind + 1], values[ind]))

    def test_lin_nn_random(self):
        values = self.rand_sorted(magnitude=1000)
        ind = lin_nearest_neighbor(500.0, values)
        abs_ind_err = abs(500.0 - values[ind])
        if ind > 0:
            self.assertTrue(abs_ind_err < abs(500 - values[ind - 1]),
                            "{0} is closer to 500 than {1}".format(values[ind - 1], values[ind]))
        if ind < len(values) - 1:
            self.assertTrue(abs_ind_err < abs(500 - values[ind + 1]),
                            "{0} is closer to 500 than {1}".format(values[ind + 1], values[ind]))

    def test_bin_nn_fixed(self):
        values = (0.9869012357855894, 0.3656084545608417, 0.5786822960723768, 0.028219408750972175, 0.12300244702440688,
                  0.83130694643633, 0.6256979816208983, 0.15799096001984392, 0.778421648132176, 0.505326751687562)
        ind = nearest_neighbor(0.8,values)
