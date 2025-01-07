"""Wrong file extension exception

- WrongFileExtensionException
"""


class WrongFileExtensionException(Exception):
    """Wrong file extension exception"""
    def __init__(self, received: str, required: str | list[str]):
        super().__init__()

        if isinstance(required, str):
            required = [required]

        if len(required) == 1:
            ending = ''
        else:
            ending = 's:'

        if len(required) <= 2:
            required = ' or '.join(required)
        else:
            required = f'{", ".join(required[:-2])}, {" or ".join(required[-2:])}'

        self._message = (
            f'You used an unsupported file extension {received}! Please use '
            f'supported file extension{ending} {required}!')

    def __str__(self):
        return self._message
