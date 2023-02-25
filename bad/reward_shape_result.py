# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long
class RewardShapeResult:
    """reward shape result"""
    def __init__(self, is_legal_action:bool) -> None:
        """init"""
        self.legal_action: int = 10 if is_legal_action is True else -10
