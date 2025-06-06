from csv_utility import CSVUtility
import argparse

# Initialize the argument parser
parser = argparse.ArgumentParser(description='CSV Utility Command Line Tool')
parser.add_argument('--input', '-i', type=str, help='Path to the CSV file. Relative to data/', required=True)
parser.add_argument('--separator', '-s',type=str, default=',', help='Separator used in the CSV file')
parser.add_argument('--encoding', '-e',type=str, default='utf-8', help='Encoding of the CSV file')
parser.add_argument('--rows', '-r',type=int, default=5, help='Number of rows to display for head/tail operations')
# Operations will be semicolon separated, order specific input
# It can contain multiple operations like head; tail; update; replace_missing; remove_empty; filter <column> <sign> <value>; aggregate <column> <operation>; sort <column> DESC/ASC; save <file_path>
parser.add_argument('--operations', '-o', type=str, default= "update;replace_missing;remove_empty;head", help='Operations to perform on the CSV file')
parser.add_argument('--op-delimiter', '-d', type=str, default=';', help='Delimiter for separating operations in the operations argument')
args = parser.parse_args()

# Create an instance of CSVUtility with the provided arguments
csv_utility = CSVUtility('data/' + args.input, separator=args.separator, encoding=args.encoding)

# Perform the requested operations

operators = {
    'head': csv_utility.get_head_data,
    'tail': csv_utility.get_tail_data,
    'update': csv_utility.update_data,
    'replace_missing': csv_utility.replace_missing_values,
    'remove_empty': csv_utility.remove_empty_rows,
    'filter': csv_utility.filter_rows,
    'aggregate': csv_utility.aggregator,
    'sort': csv_utility.sort_rows,
    'save': csv_utility.save_data,
}
rows = args.rows if args.rows > 0 else 5

index = 0
operations = args.operations.split(args.op_delimiter)

for index in range(len(operations)):
    operation = operations[index].strip().lower().split()[0]
    if operation in operators:

        if operation in {'head', 'tail'}:
            result = operators[operation](rows)
            print(f"Printing {operation} data with {rows} rows.")
            print(result)
        
        elif operation.startswith('save'):
            res = operations[index].split()
            file_path = "data/" + res[1]
            operators[operation](file_path)
            print(f"Data saved to {file_path}")

        elif operation.startswith('filter'):
            res = operations[index].split()
            if len(res) != 4:
                raise IndexError("Filter operation requires a column_name, operator, and value.")
            filter_condition = ' '.join(res[1:])
            operators[operation](filter_condition)

        elif operation.startswith('aggregate'):
            res = operations[index].split()
            if len(res) != 3:
                raise IndexError("Aggregate operation requires a column_name and an aggregation operation.")
            column, agg_operation = res[1], res[2]
            value = operators[operation](column, agg_operation)
            print(f"Aggregation result for column '{column}' with operation '{agg_operation}': {value}")
        
        elif operation.startswith('sort'):
            res = operations[index].split()
            if len(res) != 3:
                raise IndexError("Sort operation requires a column_name and an order (ASC/DESC)")

            sort_column, sort_order = res[1], res[2].upper()
            if sort_order not in {'ASC', 'DESC'}:
                raise ValueError(f"Invalid sort order: {sort_order}. Use 'ASC' or 'DESC'.")
            operators[operation](sort_column, sort_order == 'ASC')
        else:
            operators[operation]()
        print(f"Operation '{operation}' completed.")
    else:
        print(f"Unknown operation: {operation}")