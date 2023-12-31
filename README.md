# basedrow

<img src="https://github.com/knowsuchagency/basedrow/blob/main/logo.png?raw=true" alt="logo.png" width="400"/>

`basedrow` is a Python wrapper around the Baserow API. It provides a simple and intuitive way to interact with Baserow databases, allowing users to perform various operations like listing rows, creating new rows, updating existing ones, and more.

## Features
- Easy to use client for interacting with the Baserow API.
- Supports listing, creating, updating, and retrieving rows in a Baserow table.
- Additional support for advanced query parameters like search, order_by, filters, etc.
- Extensible design for easy integration with other Python applications.

## Installation

To install `basedrow`, you can use pip:

```bash
pip install basedrow
```

## Usage

### Working with Tables

```python
from basedrow import Client, Table

client = Client(url='YOUR_BASEROW_URL', token='YOUR_API_TOKEN')

# Initialize a table
table = Table(table_id='YOUR_TABLE_ID', client=client)

# List rows in the table
rows = table.list_rows()

# Filter rows
filtered_rows = table.list_rows(
    # fields starting with `filter__{col}__{op}` will be converted to filters
    # see Baserow the API documentation for your table for details
    filter__name__contains='sam',
)

# Get a specific row
row = table.get_row(row_id='ROW_ID')

# Create a new row
new_row = table.create_row(row={'column_name': 'value'})

# Update existing rows
updated_rows = table.update_rows(rows=[{'id': 'ROW_ID', 'column_name': 'new_value'}])
```

### Windmill Integration

```python
from basedrow import WindmillClient
client = WindmillClient(resource="f/your/baserowresource")
```

## Contributing

Contributions to `basedrow` are welcome! Please read our contributing guidelines to get started.

## License

`basedrow` is licensed under the [MIT License](LICENSE).
