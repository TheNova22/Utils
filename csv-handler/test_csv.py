import unittest
from csv_utility import CSVUtility
import pandas as pd
class TestCSVUtility(unittest.TestCase):
    def setUp(self):
        # Initialize CSVUtility with a sample CSV file for testing
        self.csv_utility = CSVUtility('data/clv_data.csv', separator=',', encoding='utf-8')

    def test_get_head_data(self):
        head_data = self.csv_utility.get_head_data(3)
        self.assertEqual(len(head_data), 3)

    def test_get_tail_data(self):
        tail_data = self.csv_utility.get_tail_data(3)
        self.assertEqual(len(tail_data), 3)

    def test_get_data(self):
        data = self.csv_utility.get_data()
        self.assertIsInstance(data, pd.DataFrame)

    def test_save_data(self):
        self.csv_utility.save_data('data/output.csv')
        saved_data = pd.read_csv('data/output.csv')
        self.assertEqual(saved_data.shape, self.csv_utility.data.shape)
    
    def test_replace_missing_values(self):
        initial_data = self.csv_utility.data.copy()
        self.csv_utility.replace_missing_values()
        # Check if missing values are replaced
        self.assertFalse(self.csv_utility.data.isnull().values.any())
        # Ensure the shape of the DataFrame remains the same
        self.assertEqual(initial_data.shape, self.csv_utility.data.shape)
    
    def test_remove_empty_rows(self):
        initial_shape = self.csv_utility.data.shape
        self.csv_utility.remove_empty_rows()
        # Check if the number of rows has decreased
        self.assertLessEqual(self.csv_utility.data.shape[0], initial_shape[0])
        # Ensure the shape of the DataFrame remains the same in terms of columns
        self.assertEqual(self.csv_utility.data.shape[1], initial_shape[1])
    
    def test_filter_rows(self):
        # Assuming the CSV has a column named 'age'
        self.csv_utility.filter_rows('age > 10')
        # Check if the filtered DataFrame has only rows where 'age' > 10
        self.assertTrue((self.csv_utility.data['age'] > 10).all())

    def test_aggregate_data(self):
        res = self.csv_utility.aggregator('age', 'mean')
        # Check if the aggregated result is a single value
        self.assertEqual(res, self.csv_utility.data['age'].mean())
    
    def test_sort_rows(self):
        self.csv_utility.sort_rows('age', ascending=True)
        # Check if the DataFrame is sorted by 'age'
        self.assertTrue(self.csv_utility.data['age'].dropna().is_monotonic_increasing)
    
if __name__ == '__main__':
    unittest.main()