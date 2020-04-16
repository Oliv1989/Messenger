"""ERRORS"""


class IncorrectDataRecivedError(Exception):
    """
    Exception - wrong data from socket
    """

    def __str__(self):
        return 'Принято некорректное сообщение от удалённого компьютера.'


class NonDictInputError(Exception):
    """
    Exception - function`s argument isn`t a dictionary
    """

    def __str__(self):
        return 'Аргумент функции должен быть словарём.'


class ReqFieldMissingError(Exception):
    """
    Error - missing obligatory field in a dictionary
    """

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'


class ServerError(Exception):
    """Exception - Server error"""

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
