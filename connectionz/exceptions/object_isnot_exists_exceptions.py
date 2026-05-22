"""Object is not exists exceptions

- ObjectIsNotExistsException
    - NodeIsNotExistsException
    - CoupleIsNotExistsException
    - EdgeIsNotExistsException
"""

from connectionz.core.identifier import Identifier


class ObjectIsNotExistsException(Exception):
    """Object is not exists exception"""
    def __init__(self, obj_name: str):
        super().__init__()
        message = f'{obj_name.strip()} is not exists!'
        self._message = message

    def __str__(self):
        return self._message


class NodeIsNotExistsException(ObjectIsNotExistsException):
    """Node is not exists exception"""
    def __init__(self):
        super().__init__('Node')


class NodeAttributeIsNotExistsException(ObjectIsNotExistsException):
    """Node attribute is not exists exception"""
    def __init__(self):
        super().__init__('Node attribute')


class CoupleIsNotExistsException(ObjectIsNotExistsException):
    """Couple is not exists exception"""
    def __init__(self):
        super().__init__('Couple')


class EdgeIsNotExistsException(ObjectIsNotExistsException):
    """Edge is not exists exception"""
    def __init__(self):
        super().__init__('Edge')


class EdgeAttributeIsNotExistsException(ObjectIsNotExistsException):
    """Edge attribute is not exists exception"""
    def __init__(self, attribute: str):
        super().__init__(f'Edge attribute "{attribute}"')


class PathBetweenNodesIsNotExistsException(ObjectIsNotExistsException):
    """Path betweeen nodes is not exists exception"""
    def __init__(self, source_node: Identifier, target_node: Identifier):
        super().__init__(f'Path betweeen nodes "{source_node}" and "{target_node}"')


class PathBetweenSameNodeCanNotExistException(Exception):
    """Path between the same node can not exist exception"""
    def __init__(self):
        super().__init__()
        message = 'Path betweeen the same node can not exists!'
        self._message = message

    def __str__(self):
        return self._message
