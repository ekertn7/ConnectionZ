"""Exceptions init"""

from . object_already_exists_exceptions import (
    NodeAlreadyExistsException,
    EdgeAlreadyExistsException)
from . object_isnot_exists_exceptions import (
    NodeIsNotExistsException,
    CoupleIsNotExistsException,
    EdgeIsNotExistsException)
from . cannot_delete_basic_elements_exceptions import (
    CanNotDeleteNodesException,
    CanNotDeleteEdgesException)
from . validation_exceptions import (
    WrongTypeOfNodesException,
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfNodeAttributesException,
    WrongTypeOfEdgesException,
    WrongTypeOfCoupleException,
    WrongLengthOfCoupleException,
    WrongTypeOfNodeIdentifierInCoupleException,
    WrongTypeOfMultipleEdgesException,
    WrongLengthOfMultipleEdgesException,
    WrongTypeOfEdgeIdentifierException,
    WrongTypeOfEdgeAttributesException,
    DuplicationInEdgeIdentifiersException)
from . wrong_file_extension_exception import (
    WrongFileExtensionException)
