"""Object is not exists exceptions

- ObjectIsNotExistsException
    - NodeIsNotExistsException
    - CoupleIsNotExistsException
    - EdgeIsNotExistsException
"""


class ObjectIsNotExistsException(Exception):
    """Object is not exists exception"""
    def __init__(self, obj_name: str):
        super().__init__()
        message = f'{obj_name.capitalize()} is not exists!'
        self._message = message

    def __str__(self):
        return self._message


class NodeIsNotExistsException(ObjectIsNotExistsException):
    """Node is not exists exception"""
    def __init__(self):
        super().__init__('node')


class CoupleIsNotExistsException(ObjectIsNotExistsException):
    """Couple is not exists exception"""
    def __init__(self):
        super().__init__('couple')


class EdgeIsNotExistsException(ObjectIsNotExistsException):
    """Edge is not exists exception"""
    def __init__(self):
        super().__init__('edge')
