## CSV Reading Utility

Like shell commands, use this utility to perform batch operations via command line

Currently run via python3 or through docker args

### Python CLI

Clone the repo and run the following after adding a CSV into data directory

```
python3 csv_reader.py -i clv_data.csv -o "head; update; replace_missing; remove_empty; head; filter income > 50000; aggregate age mean; save new_data.csv"

python3 csv_reader.py -i new_data.csv -o "sort age DESC; save new_data2.csv"
```

### Docker CLI

Clone the repo, build the image and run the following command

```
docker build -t csv_utility:latest .
docker run --name csv-util \
 -d -v "$(pwd)/data:/data" csv_utility \
 -i clv_data.csv \
 -o "head; update; replace_missing; remove_empty; head; filter income > 50000; save data_docker.csv"

docker logs csv-util
```

## Content

The scipts are mainly divided into 3 python files

1.  csv\_utility.py - Main Class File containing all the necessary functions, makes use of pandas
2.  csv\_ready.py - Parser + Interactor file. Instantiates an object and formats user args to call the utility functions
3.  test\_csv.py - Unittest file written to check if utility functions give the right output or not
    1.  Perform the tests by running the python file

### Data

Any sort of csv reference and usage is done from the data/ directory. Hence, it is advised to mount the directory when running it as a docker container.

It contains a clv\_dataset taken from here: [https://www.kaggle.com/datasets/kenjee/simulated-missing-value-and-outlier-data/data](https://www.kaggle.com/datasets/kenjee/simulated-missing-value-and-outlier-data/data) 

### Options

The parser is currently written with the following options

| Param | Param | Description | Default |
| --- | --- | --- | --- |
| \--input | \-i | Path to the CSV file. Relative to data/ | None |
| \--separator | \-s | Separator used in the CSV file | , |
| \--encoding | \-e | Encoding of the CSV file | utf-8 |
| \--rows | \-r | Number of rows to display for head/tail operations | 5 |
| \--operations | \-o | List of operations to be performed (order matters) | update;replace\_missing;remove\_empty;head |
| \--op-delimiter | \-d | Delimiter for separating operations in the operations argument | ; |

### Oprations

<table><tbody><tr><td>Operation</td><td>Format</td></tr><tr><td>Print top/head of the data</td><td>head;</td></tr><tr><td>Print bottom/tail of the data</td><td>tail;</td></tr><tr><td>Replace missing values with NaN</td><td>update;</td></tr><tr><td>Replace NaN with mean/mode</td><td>replace_missing;</td></tr><tr><td>Remove empty rows</td><td>remove_empty;</td></tr><tr><td>Filter data according to a column's value</td><td><p>filter &lt;column&gt; &lt;sign&gt; &lt;value&gt;;</p><p>Supported signs: &gt; &lt; &lt;= &gt;= ==</p></td></tr><tr><td>Sort data according to a column</td><td>sort &lt;column&gt; DESC/ASC;</td></tr><tr><td>Aggregate data of a column and get answer</td><td><p>aggregate &lt;column&gt; &lt;operation&gt;;</p><p>Operations: sum, mean, min, max, count, product, std, var</p></td></tr><tr><td>Save data</td><td><p>save &lt;output.csv&gt;;</p><p>Gets saved relative to data/</p></td></tr></tbody></table>

### Example Output

```
Operations: "head; update; replace_missing; remove_empty; head; filter income > 50000; aggregate age mean; save new_data.csv"

Printing head data with 5 rows.
   Unnamed: 0  id   age  gender  income  days_on_platform           city  purchases
0           0   0   NaN    Male  126895              14.0  San Francisco          0
1           1   1   NaN    Male  161474              14.0          Tokyo          0
2           2   2  24.0    Male  104723              34.0         London          1
3           3   3  29.0    Male   43791              28.0         London          2
4           4   4  18.0  Female  132181              26.0         London          2
Operation 'head' completed.
Operation 'update' completed.
Operation 'replace_missing' completed.
Operation 'remove_empty' completed.
Printing head data with 5 rows.
   Unnamed: 0  id        age  gender  income  days_on_platform           city  purchases
0           0   0  30.202036    Male  126895              14.0  San Francisco          0
1           1   1  30.202036    Male  161474              14.0          Tokyo          0
2           2   2  24.000000    Male  104723              34.0         London          1
3           3   3  29.000000    Male   43791              28.0         London          2
4           4   4  18.000000  Female  132181              26.0         London          2
Operation 'head' completed.
Operation 'filter' completed.
Aggregation result for column 'age' with operation 'mean': 30.259112597025485
Operation 'aggregate' completed.
Data saved to data/new_data.csv
Operation 'save' completed.
```