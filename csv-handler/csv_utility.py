# Command line utility-esque program that will perform functionalities via arguments passed
# Have action flags in place to perform the required actions
# Default values for particular actions will be set
# Filter Rows Based on Criteria - Provide column name and condition like "column_name>value" or "column_name<value" or "column_name=value"
# Empty rows and improper formats will be dropped
# Missing values will be handled by dropping or filling them based on user preference

# Utilize argparse for command line argument parsing
# Utilize pandas for data manipulation and analysis

import pandas as pd
class CSVUtility:
    def __init__(self, file_path, separator=',', encoding='utf-8'):
        self.file_path = file_path
        self.data = pd.read_csv(file_path, sep=separator, encoding=encoding)
    
    def get_head_data(self, rows: int = 5) -> pd.DataFrame:
        """
        Get the first few rows of the CSV file.
        :param rows: Number of rows to return
        :return: DataFrame containing the first few rows
        """
        return self.data.head(rows)

    def get_tail_data(self, rows: int = 5) -> pd.DataFrame:
        """
        Get the last few rows of the CSV file.
        :param rows: Number of rows to return
        :return: DataFrame containing the last few rows
        """
        return self.data.tail(rows)
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the entire DataFrame.
        :return: DataFrame containing all data
        """
        return self.data

    def save_data(self, file_path, index = False):
        """
        Save the current DataFrame to a new CSV file.
        :param file_path: Path to save the new CSV file
        """
        self.data.to_csv(file_path, index= index)

    def update_data(self):
        """
        Update the data in the DataFrame.
        This method can be extended to include more complex data manipulation.
        """
        for col in self.get_columns():
            # If the column is completely empty, drop it
            if self.data[col].isnull().all():
                self.data.drop(columns=[col], inplace=True)
                continue
            
            # If any row in the column is empty, fill it with NaN
            if pd.api.types.is_numeric_dtype(self.data[col]):
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            else:
                # If it isn't numeric, convert it to string
                self.data[col] = self.data[col].astype(str)
    
    def replace_missing_values(self):
        """
        Replace missing values in the DataFrame with mean for numeric columns, mode for categorical columns.
        """
        # Get the columns with missing values
        # Columns with number type will be made into average
        missing_cols = self.data.columns[self.data.isnull().any()]
        for col in missing_cols:
            if pd.api.types.is_numeric_dtype(self.data[col]):
                self.data[col] = self.data[col].fillna(self.data[col].mean())
            else:
                # Replace with mode for categorical columns
                self.data[col] = self.data[col].fillna(self.data[col].mode()[0])

    def remove_empty_rows(self):
        """
        Remove empty rows from the DataFrame.
        """
        self.data.dropna(how='all', inplace=True)
        self.data.reset_index(drop=True, inplace=True)
    
    def sort_rows(self, column_names, ascending=True, replace = True):
        """
        Sort the rows based on specific columns.
        :param column_names: Columns to sort by
        :param ascending: Sort in ascending order if True, else descending
        :param replace: If True, replace the current data with sorted data, else print the sorted data
        """
        new_data = self.data.sort_values(by=column_names, ascending=ascending)
        new_data.reset_index(drop=True, inplace=True)
        if replace:
            self.data = new_data
        else:
            print(new_data.head(10))
    
    def filter_rows(self, condition):
        """
        Filter rows based on a condition.
        :param column_name: Column to filter by
        :param condition: Condition to apply (e.g., "column_name>value")
        :return: Filtered DataFrame
        """
        column_name, sign, value = condition.split(' ')
        if sign not in {'>', '<', '==', '>=', '<='}:
            raise ValueError("Invalid condition sign. Use one of: >, <, ==, >=, <=")
        if pd.api.types.is_numeric_dtype(self.data[column_name]):
            value = float(value)
        elif pd.api.types.is_string_dtype(self.data[column_name]):
            value = "'" + str(value) + "'"
        else:
            raise ValueError(f"Unsupported data type for column '{column_name}'")
        bool_rows = self.data.eval(f"{column_name} {sign} {value}")
        filtered_data = self.data[bool_rows]
        self.data = filtered_data.reset_index(drop=True)
        
    
    def get_columns(self):
        """
        Get the list of columns in the DataFrame.
        :return: List of column names
        """
        return self.data.columns.tolist()
    
    def aggregator(self, column_name, operation='sum'):
        """
        Perform aggregation on a specific numeric column.
        :param column_name: Column to perform aggregation on
        :param operation: Aggregation operation (e.g., 'sum', 'mean', 'min', 'max')
        :return: Aggregated value
        """
        if column_name not in self.data.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        # Supported operations: sum, mean, min, max, count, product, std, var
        operation_dict = {
            "sum": self.data[column_name].sum,
            "mean": self.data[column_name].mean,
            "min": self.data[column_name].min,
            "max": self.data[column_name].max,
            "count": self.data[column_name].count,
            "product": self.data[column_name].prod,
            "std": self.data[column_name].std,
            "var": self.data[column_name].var
        }
        if operation not in operation_dict:
            raise ValueError(f"Unsupported operation '{operation}'. Supported operations: {list(operation_dict.keys())}")
        
        operator = operation_dict[operation]
        return operator()