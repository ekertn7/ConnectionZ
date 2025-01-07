"""Can not delete basic elements in graph exceptions

- CanNotDeleteBasicElementsInGraphException
    - CanNotDeleteNodesException
    - CanNotDeleteEdgesException
"""


class CanNotDeleteBasicElementsInGraphException(Exception):
    """Can not delete basic elements in graph exception"""
    def __init__(self, element: str):
        super().__init__()
        self._message = (
            f'You can not delete basic elements in graph, like nodes or edges! '
            f'If you want to delete all {element}, use clear_{element} method '
            f'instead of del!')

    def __str__(self):
        return self._message


class CanNotDeleteNodesException(CanNotDeleteBasicElementsInGraphException):
    """Can not delete nodes exception"""
    def __init__(self):
        super().__init__(element='nodes')


class CanNotDeleteEdgesException(CanNotDeleteBasicElementsInGraphException):
    """Can not delete edges exception"""
    def __init__(self):
        super().__init__(element='edges')
