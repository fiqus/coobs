import unittest
import unittest.mock

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
#TODO not being used
# def spy_decorator(method_to_decorate):
    # mock = unittest.mock.MagicMock()
    # def wrapper(self, *args, **kwargs):
        # mock(*args, **kwargs)
        # return method_to_decorate(self, *args, **kwargs)
    # wrapper.mock = mock
    # return wrapper