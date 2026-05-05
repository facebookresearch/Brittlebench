"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.perturbation import TextPerturbation


class PaddingPerturbation(TextPerturbation):
    def __init__(self,
                 char_count: int = 0,
                 char: str = ""):
        super().__init__()
        self.char = char
        self.char_count = char_count

    def apply(self, text: str) -> str:
        """
        Appends and prepends a specified character a given number of times.
        """
        return f'{self.char * self.char_count} {text} {self.char * self.char_count}'
