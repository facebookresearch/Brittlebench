"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random
from typing import List, Union, Optional, Tuple

from brittlebench.perturbations.perturbation import ListPerturbation


class ShuffleOrderPerturbation(ListPerturbation):

    def __init__(self, seed: Optional[int] = None,):
        super().__init__()
        self.seed = seed

    def apply(self, 
              choices: List[str], 
              answer: Union[str, int]
              ) -> Tuple[List[str], Union[str, int]]:
        if not choices:
            raise ValueError("Choices list cannot be empty.")

        # Create a list of (original_index, option) pairs
        indexed_options = list(enumerate(choices))
        shuffled = random.sample(indexed_options, k=len(indexed_options))
        shuffled_options = [opt for _, opt in shuffled]

        # Helper: map letter to index
        def letter_to_index(letter: str) -> int:
            letter = letter.upper()
            idx = ord(letter) - ord('A')
            if idx < 0 or idx >= len(choices):
                raise ValueError(f"Letter '{letter}' is out of range for choices.")
            return idx

        # Helper: map index to letter
        def index_to_letter(idx: int) -> str:
            if idx < 0 or idx >= len(choices):
                raise ValueError(f"Index '{idx}' is out of range for choices.")
            return chr(ord('A') + idx)

        # Remap answer
        if isinstance(answer, int):
            if answer < 0 or answer >= len(choices):
                raise ValueError(f"Answer index '{answer}' is out of range for choices.")
            # Find where the original index ended up in the shuffled list
            new_index = next(i for i, (orig_idx, _) in enumerate(shuffled) if orig_idx == answer)
            updated_answer = new_index
        elif isinstance(answer, str):
            # Is it a single letter?
            if len(answer) == 1 and answer.isalpha():
                orig_index = letter_to_index(answer)
                new_index = next(i for i, (orig_idx, _) in enumerate(shuffled) if orig_idx == orig_index)
                updated_answer = index_to_letter(new_index)
            # Is it the full string? Return as-is
            elif answer in choices:
                updated_answer = answer
            else:
                raise ValueError(f"Answer string '{answer}' not found in choices.")
        else:
            raise TypeError("Answer must be int (index) or str (letter or choice string).")

        return shuffled_options, updated_answer
