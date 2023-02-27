# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, consider-using-enumerate, line-too-long, line-too-long
class Baseline:
    """baseline"""
    def __init__(self, mean:float, std: float) -> None:
        """init"""
        self.mean = mean
        self.std = std
