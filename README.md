# mysql-helper

`mysql-helper` is a Python package designed to simplify various MySQL database operations. It provides easy connection management and data manipulation, making it ideal for development and testing environments where quick, one-off executions are needed.

## Features

- **Easy Configuration**: Connect to MySQL databases using a configuration file, a dictionary, or direct parameters.
- **Connection Management**: Automatically handles connection setup and teardown, with built-in error handling and transaction support.
- **Query Utilities**: Provides helper functions for common database operations like fetching data and retrieving table metadata.

## Installation

To install the package locally using pip, navigate to the project directory and run:

```bash
pip install .
```

## Usage

The `db_connector` decorator simplifies the process of managing database connections in your Python functions. It is designed for scenarios where database connections are short-lived, making it suitable for development, testing, and one-off scripts.

### Example

Below is an example of how to use the `db_connector` decorator to interact with a MySQL database.

```python
from mysqlhelper import db_connector

@db_connector(host='127.0.0.1', port='3306', 
              user='root', password='123456', database='my_db')
def demo(cursor):
    """
    A demo function that queries the first 30 rows from the 'my_table' table.

    Args:
        cursor: MySQL cursor object provided by the `db_connector` decorator.

    Returns:
        list: A list of dictionaries, each representing a row from the result set.
    """
    # Execute a SQL query to fetch the first 30 rows from 'my_table'
    cursor.execute('SELECT * FROM my_table LIMIT 30')

    # Fetch all results as a list of dictionaries
    results = cursor.fetchall()
    
    return results

# Run the demo function and print the results
if __name__ == "__main__":
    data = demo()
    for row in data:
        print(row)
```

In this example, the `db_connector` decorator automatically provides a `cursor` object to the decorated function, which can be used to execute SQL queries and fetch results.  
This approach is ideal for development and testing, where quick, ad-hoc database interactions are needed without the overhead of maintaining long-lived connections or managing complex connection pools.
