from colorama import Fore


class ColorIsNotExists(Exception):
    """Возникает если переданный цвет в логгер не существует

    Атрибуты:
        msg -- описание ошибки
    """

    def __init__(self, msg):
        self.msg = msg


class EqualColors(Exception):
    """Возникакет если обнаружились повторяющиеся цвета

    Атрибуты:
        msg -- описание ошибки
    """

    def __init__(self, msg: str):
        self.msg = msg


class Logger:
    def __init__(self, info_color="blue", warning_color="yellow", error_color="red"):
        self.__colors = Fore.__dict__

        colors = list(map(str.upper, [info_color, warning_color, error_color]))
        for i in colors:
            if i not in self.__colors:
                raise ColorIsNotExists(f"{i} не существует")
            if colors.count(i) != 1:
                raise EqualColors(f"{i} не может быть урп")

        self.__info_color = str.upper(info_color)
        self.__warning_color = str.upper(warning_color)
        self.__error_color = str.upper(error_color)

    def info(self, msg: str, end='\n'):
        print(f"{self.__colors[self.__info_color]} [INFO] {msg} {self.__colors['RESET']}", end=end)

    def warning(self, msg: str, end='\n'):
        print(f"{self.__colors[self.__warning_color]} [WARNING] {msg} {self.__colors['RESET']}", end=end)

    def error(self, msg: str, end='\n'):
        print(f"{self.__colors[self.__error_color]} [ERROR] {msg} {self.__colors['RESET']}", end=end)

    def print(self, msg: str, color='BLUE', end='\n', tag=''):
        color = str.upper(color)
        if color not in self.__colors:
            raise ColorIsNotExists(f"{color} не существует")
        print(f"{self.__colors[color]}{tag} {msg}{self.__colors['RESET']}", end=end)
