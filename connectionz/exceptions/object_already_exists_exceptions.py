"""Object already exists exceptions

- ObjectAlreadyExistsException
    - NodeAlreadyExistsException
    - EdgeAlreadyExistsException
"""


class ObjectAlreadyExistsException(Exception):
    """Object already exists exception"""
    def __init__(self, obj_name: str):
        super().__init__()
        message = (
            f'{obj_name.capitalize()} already exists! Please, change parameter '
            f'`replace` to true if you want to replace this {obj_name.lower()} '
            f'by new!')
        self._message = message

    def __str__(self):
        return self._message


class NodeAlreadyExistsException(ObjectAlreadyExistsException):
    """Node already exists exception"""
    def __init__(self):
        super().__init__('node')


class EdgeAlreadyExistsException(ObjectAlreadyExistsException):
    """Edge already exists exception"""
    def __init__(self):
        super().__init__('edge')
