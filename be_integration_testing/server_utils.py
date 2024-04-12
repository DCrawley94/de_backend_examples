def format_response(columns, data, label):
    """Formats the rows returned from a pg8000 query"""
    if len(data) > 1:
        formatted_data = [dict(zip(columns, row)) for row in data]
    else:
        formatted_data = dict(zip(columns, data[0]))
    return {label: formatted_data}