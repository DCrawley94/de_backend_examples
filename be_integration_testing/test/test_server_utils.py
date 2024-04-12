from server_utils import format_response

def test_format_response_should_format_single_row():
    columns = ['a', 'b', 'c']
    rows = [[1,2,3]]
    label = 'test_label'

    expected = {
        'test_label': {
            'a': 1,
            'b': 2,
            'c': 3
        }
    }

    assert format_response(columns, rows, label) == expected


def test_format_response_should_format_multi_rows():
    columns = ['a', 'b', 'c']
    rows = [[1,2,3], [4,5,6]]
    label = 'test_label'

    expected = {
        'test_label': [
            {
                'a': 1,
                'b': 2,
                'c': 3
            }, {
                'a': 4,
                'b': 5,
                'c': 6
            }
        ]
    }

    assert format_response(columns, rows, label) == expected