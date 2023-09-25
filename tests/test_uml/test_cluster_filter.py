import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import cluster_filter

class TestClusterFilter(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'go': [72, 52, 37, 51, 99, 14, 27, 41, 72, 95, 47, 97, 71, 78, 31, 3, 87, 26, 10, 64, 47, 21, 25, 74, 35, 91, 94, 5, 36, 86, 21, 11, 68, 55, 51, 36, 27, 22, 71, 31, 42, 79, 51, 8, 31, 41, 10, 7, 81, 84, 19, 59, 54, 45, 22, 93, 79, 50, 62, 57, 76, 94, 20, 93, 35, 0, 38, 36, 18, 79, 89, 3, 67, 16, 95, 57, 90, 40, 82, 2, 37, 25, 75, 41, 13, 97, 15, 58, 70, 59, 7, 4, 55, 21, 37, 6, 23, 85, 84, 83],
            'elect': [3, 60, 37, 16, 6, 41, 19, 30, 68, 78, 4, 19, 10, 19, 29, 39, 58, 4, 65, 66, 27, 51, 44, 24, 22, 28, 51, 65, 9, 72, 84, 97, 55, 21, 48, 96, 77, 65, 36, 30, 55, 15, 29, 56, 21, 25, 65, 9, 40, 65, 7, 35, 33, 82, 46, 5, 23, 78, 33, 17, 74, 50, 85, 61, 91, 55, 13, 93, 29, 39, 92, 95, 97, 10, 16, 51, 30, 95, 21, 11, 54, 88, 73, 11, 54, 6, 36, 88, 38, 97, 35, 28, 28, 35, 17, 93, 42, 63, 98, 39],
            'local': [94, 56, 24, 92, 5, 43, 21, 45, 32, 75, 5, 80, 31, 40, 62, 64, 83, 41, 69, 54, 7, 60, 97, 12, 18, 14, 94, 21, 26, 9, 86, 63, 5, 5, 74, 58, 67, 44, 70, 21, 15, 49, 26, 1, 1, 49, 99, 77, 37, 14, 3, 95, 59, 27, 68, 9, 98, 66, 78, 46, 37, 50, 13, 0, 51, 37, 82, 16, 61, 46, 11, 94, 12, 64, 32, 67, 73, 41, 99, 96, 35, 66, 87, 42, 12, 29, 7, 3, 49, 62, 68, 0, 42, 16, 83, 38, 53, 73, 68, 70],
            'etot': [83, 5, 97, 28, 90, 58, 56, 64, 85, 7, 63, 40, 51, 12, 33, 67, 99, 80, 59, 77, 64, 90, 66, 24, 2, 75, 8, 60, 85, 70, 9, 34, 24, 83, 45, 94, 65, 47, 61, 14, 39, 93, 74, 3, 36, 4, 74, 31, 30, 38, 6, 69, 19, 56, 18, 8, 71, 83, 7, 84, 93, 60, 53, 15, 58, 98, 6, 64, 87, 69, 71, 24, 7, 41, 68, 14, 75, 21, 36, 40, 4, 25, 86, 73, 67, 59, 0, 34, 70, 48, 68, 33, 1, 18, 35, 58, 58, 8, 20, 47],
            'afmcc': [74, 23, 13, 46, 90, 55, 93, 13, 0, 10, 63, 87, 56, 8, 28, 75, 28, 32, 30, 49, 78, 76, 67, 41, 50, 40, 16, 82, 82, 95, 40, 19, 11, 75, 20, 15, 14, 50, 21, 58, 51, 98, 51, 37, 62, 99, 63, 61, 81, 45, 32, 79, 77, 16, 88, 81, 39, 92, 69, 57, 20, 52, 24, 82, 69, 17, 65, 29, 72, 66, 39, 37, 72, 14, 1, 95, 72, 99, 85, 22, 57, 35, 35, 2, 78, 17, 95, 15, 61, 70, 99, 35, 62, 54, 1, 1, 22, 79, 61, 96],
            'afmfit': [19, 74, 8, 49, 68, 40, 17, 8, 48, 68, 54, 66, 96, 75, 61, 98, 89, 47, 11, 38, 11, 69, 28, 64, 55, 18, 5, 27, 38, 26, 71, 52, 77, 11, 46, 8, 90, 55, 39, 16, 9, 99, 18, 30, 15, 6, 48, 19, 3, 25, 31, 24, 97, 16, 10, 20, 81, 26, 52, 68, 19, 99, 43, 35, 87, 6, 9, 73, 33, 37, 61, 72, 95, 54, 92, 58, 24, 85, 17, 5, 99, 81, 53, 14, 35, 36, 70, 69, 40, 0, 42, 11, 26, 5, 26, 55, 1, 77, 29, 49],
        })
        self.expected_output = pd.DataFrame({
            'go': [40],
            'elect': [95],
            'local': [41],
            'etot': [21],
            'afmcc': [99],
            'afmfit': [85],
        })
        
    def test_energy_filter_step(self):
        # Test the filtering logic
        filtered_df = cluster_filter(self.df)
        self.assertTrue(filtered_df.reset_index(drop=True).equals(self.expected_output))

if __name__ == '__main__':
    unittest.main()