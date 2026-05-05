"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.perturbation import TextPerturbation


class AddSpaceSeqPerturbation(TextPerturbation):
    """
    Adds random length space sequences in random places in the text based on a probability.

    Args:
        text: The input string.
        prob: The probability (0.0 to 1.0) of adding a space sequence after any given character.
        min_spaces: The minimum number of spaces to add (inclusive).
        max_spaces: The maximum number of spaces to add (inclusive).
    """

    def __init__(self, prob: float = 0.1, min_spaces: int = 1, max_spaces: int = 10):
        super().__init__()
        self.prob = prob
        self.min_spaces = min_spaces
        self.max_spaces = max_spaces


    def apply(self, text: str,) -> str:
        if not (0.0 <= self.prob <= 1.0):
            raise ValueError("Probability must be between 0.0 and 1.0")
        if self.min_spaces > self.max_spaces:
            raise ValueError("min_spaces cannot be greater than max_spaces")

        result = []
        for char in text:
            result.append(char)
            # Check if a space sequence should be added based on the probability
            if random.random() < self.prob:
                # Choose a random length for the space sequence between min and max (inclusive)
                space_length = random.randint(self.min_spaces, self.max_spaces)
                result.append(' ' * space_length)

        return "".join(result)