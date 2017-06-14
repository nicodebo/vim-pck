"""
Ansi escape sequence module
Ref: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
"""

import re
from enum import Enum


class EscapeSeq(Enum):
    """Base class for the ansi escape sequence Enumeration"""

    @staticmethod
    def reset():
        """Wrapper that return ansi reset escape sequence

        Not inside a particular Enum class as it is a commun escape sequence
        for Colors and Decoration
        """
        return "\u001b[0m"

    def describe(self):
        """Return the name and the value of the current Enum"""
        return self.name, self.value

    def enclose(self, string):
        """Enclose with the current Enum value on the left and ansi reset on
        the right
        """

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


class Parser:
    """Search and replace code with escape sequence

    Attributs:
            - lhs (str): left hand side
            - rhs (str): right hand side
            - ansi_enums (list(object instance)): list of enumerations
              defining the escape sequence


    There is hard containers/contains relashionship between this class and the
    enum classes.

    ex:
    "<bold>some text<reset>"
    the sub method parse and replace with the corresponding ansi escape
    sequence --> "\u001b[1msome text\u001b[0m"
    The lhs and rhs allow to customize the way the parsed ansi are
    represented. For exemple "[bold]some text[reset]" with lhs = '[' and
    rhs = ']'

    """

    def __init__(self, lhs='<', rhs='>'):
        self.lhs = lhs
        self.rhs = rhs
        self.ansi_enums = list(Colors16) + list(Decoration)
        self.ansi_corr = self.create_table()

    def wrap(self, string):
        """wrap string between lhs and rhs"""
        return "{0}{1}{2}".format(self.lhs, string, self.rhs)

    def create_table(self):
        """ Create a correspondance table between ansi representation and the
        real escape sequence
        ex:
        if lhs and rhs are set to default values
            | <red>  | \u001b[1m |
            | <bold> | \u001b[0m |
            | ...    | ...       |
        """
        ansi_corr = {}  # Ansi correspondance dictionnary initialization
        ansi_corr[self.wrap('reset')] = EscapeSeq.reset()  # map reset
        # map Colors16 and Decoration values
        for elem in self.ansi_enums:
            ansi_corr[self.wrap(elem.name)] = elem.value
        return ansi_corr

    def sub(self, text):
        """ Replace in 'text' all occurences of any key in the given
        dictionary by its corresponding value. Returns the new string.

        http://code.activestate.com/recipes/81330-single-pass-multiple-replace/
        """

        # Create a regular expression from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape,
                                                 self.ansi_corr.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: self.ansi_corr[mo.string[mo.start():mo.end()]], text)

    def __del__(self):
        # make sure to reset the terminal state back to default
        # does not seem to matter for zsh but important for bash
        print(EscapeSeq.reset())


# Quick exemple usage
if __name__ == "__main__":
    # 1st method: with the enum method 'enclose'
    for color in Colors16:
        name, ansi = color.describe()
        if name[0].islower():
            print(color.enclose("some {} text".format(name)))
        else:
            print(color.enclose("some bold {} text".format(name.lower())))

    for deco in Decoration:
        name, ansi = deco.describe()
        print(deco.enclose("some {} text".format(name)))

    # 2nd method: with the Parser class
    ansi_parser = Parser()
    print(ansi_parser.ansi_corr)
    ex_text = "<underline><red>some text<reset>"
    print(ansi_parser.sub(ex_text))

