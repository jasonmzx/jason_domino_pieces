from domino.testing import piece_dry_run
import base64
import json


def test_httprequestlist_get():
    input_data = {
        'urls': [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
        ],
        'method': 'GET'
    }
    piece_output = piece_dry_run(
        piece_name="HttpRequestListPiece",
        input_data=input_data
    )
    results = piece_output['base64_bytes_data_list']
    assert len(results) == 2
    for encoded in results:
        data = json.loads(base64.decodebytes(encoded.encode('utf-8')))
        assert 'id' in data


def test_httprequestlist_post():
    input_data = {
        'urls': [
            'https://httpbin.org/post',
            'https://httpbin.org/post',
        ],
        'method': 'POST',
        'body_json_data': json.dumps({
            'key_1': 'domino',
            'key_2': 'testing-list-post'
        })
    }
    piece_output = piece_dry_run(
        piece_name="HttpRequestListPiece",
        input_data=input_data
    )
    results = piece_output['base64_bytes_data_list']
    assert len(results) == 2
    for encoded in results:
        data = json.loads(base64.decodebytes(encoded.encode('utf-8')))
        assert data['json']['key_1'] == 'domino'
        assert data['json']['key_2'] == 'testing-list-post'
