import json


def check_response(response=None, expected_status=200):
    """
    Check the response from API calls to determine if they succeeded and
    if not, why.
    """
    code = response.status_code
    try:
        json.loads(response.content.decode('utf-8'))
        # TODO: look for 'success'
    except:
        print('unable to parse response (this is probably okay)')
    if code != expected_status:
        e = Exception('Expected {} but got {}'.format(expected_status, code))
        e.response = response
        print(response.text)
        raise e
    return True
