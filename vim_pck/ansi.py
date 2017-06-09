"""
Ansi escape sequence module
Ref: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
"""

from enum import Enum


class EscapeSeq(Enum):

    @staticmethod
    def reset():
        """Wrapper that return ansi reset escape sequence

        Not inside a particular Enum class as it is a commun escape sequence
        for Colors and Decoration
        """
        return "\u001b[0m"

    def describe(self):
        return self.name, self.value

    def enclose(self, string):
        escaped_string = "{}{}{}".format(self.describe()[1],
                                         string,
                                         self.reset())
        return escaped_string


class Colors16(EscapeSeq):
    """Ansi escape sequence for the 16 base colors"""

    # 8 colors normal
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    # 8 bright color
    Black = "\u001b[30;1m"
    Red = "\u001b[31;1m"
    Green = "\u001b[32;1m"
    Yellow = "\u001b[33;1m"
    Blue = "\u001b[34;1m"
    Magenta = "\u001b[35;1m"
    Cyan = "\u001b[36;1m"
    White = "\u001b[37;1m"


class Decoration(EscapeSeq):
    """Ansi escape sequence for the text decoration"""

    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"


# Quick exemple usage
if __name__ == "__main__":
    for color in Colors16:
        name, ansi = color.describe()
        if name[0].islower():
            print(color.enclose("some {} text".format(name)))
        else:
            print(color.enclose("some bold {} text".format(name.lower())))

    for deco in Decoration:
        name, ansi = deco.describe()
        print(deco.enclose("some {} text".format(name)))

