# pylint: disable=missing-module-docstring, wrong-import-position, unused-variable, unused-argument, not-callable, invalid-name, too-few-public-methods

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)


from bad.encoding.colortointconverter import ColorToIntConverter
from bad.encoding.rem_cards_to_int_converter import NumRemCardsToIntConverter


class CardProbabilitiy:
    '''card'''

    def __init__(self, color: str, num_rem_cards: int) -> None:
        rem_cards_converter: NumRemCardsToIntConverter = NumRemCardsToIntConverter()
        self.num_rem_cards = rem_cards_converter.convert(num_rem_cards)
        color_converter: ColorToIntConverter = ColorToIntConverter()
        self.color = color_converter.convert(color)


def main():
    '''main'''
    card: CardProbabilitiy = CardProbabilitiy('R', 1)
    print(card.num_rem_cards)
    print(card.color)


if __name__ == "__main__":
    main()
