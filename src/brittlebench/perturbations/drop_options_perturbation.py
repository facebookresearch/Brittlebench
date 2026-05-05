"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

import random
from git import List, Union, Optional, Tuple
from brittlebench.perturbations.perturbation import ListPerturbation


import random
from typing import List, Optional, Union, Tuple

class DropOptionsPerturbation(ListPerturbation):
    """
    Drops a fraction of the options from a list of multiple choice options.
    If is_poe=True, returns a random wrong answer from the reduced set.
    """
    def __init__(
        self, 
        target_option_count: int = 2,
        seed: Optional[int] = None,
        is_poe: bool = False
    ):
        super().__init__()
        self.target_option_count = target_option_count
        self.seed = seed
        self.is_poe = is_poe

    def _resolve_answer(self, choices: List[str], answer: Union[int, str]) -> Tuple[int, str]:
        """Return (index, format_type) for the answer."""
        n = len(choices)
        if isinstance(answer, int):
            if 0 <= answer < n:
                return answer, 'index'
            raise ValueError(f"Answer index {answer} out of range.")
        if isinstance(answer, str):
            if answer in choices:
                return choices.index(answer), 'string'
            if len(answer) == 1 and answer.upper().isalpha():
                idx = ord(answer.upper()) - ord('A')
                if 0 <= idx < n:
                    return idx, 'letter'
                raise ValueError(f"Letter '{answer}' out of range for list of length {n}.")
            raise ValueError(f"Answer '{answer}' not found in choices.")
        raise ValueError("Answer must be int or str.")

    def _format_answer(self, fmt: str, idx: int, choices: List[str]) -> Union[int, str]:
        """Format answer index as original type."""
        if fmt == 'index':
            return idx
        if fmt == 'letter':
            return chr(ord('A') + idx)
        if fmt == 'string':
            return choices[idx]
        raise ValueError(f"Unknown answer format: {fmt}")

    def apply(
        self, 
        choices: List[str], 
        answer: Union[int, str]
    ) -> Tuple[List[str], Union[int, str]]:
        """
        Reduces a list of options to a desired length, always retaining the correct answer
        unless is_poe=True, in which case a random wrong answer is returned.
        """
        if self.target_option_count < 1:
            raise ValueError("target_option_count must be at least 1.")

        n = len(choices)
        correct_index, answer_fmt = self._resolve_answer(choices, answer)
        rng = random.Random(self.seed) if self.seed is not None else random

        # Determine which indices to keep
        if self.target_option_count >= n:
            chosen_indices = list(range(n))
        else:
            # Always keep the correct answer, fill up with random wrongs
            non_correct = [i for i in range(n) if i != correct_index]
            chosen_indices = [correct_index] + rng.sample(non_correct, self.target_option_count - 1)
            chosen_indices.sort()  # preserve original order

        new_choices = [choices[i] for i in chosen_indices]
        correct_new_index = chosen_indices.index(correct_index)

        # Select which answer to return
        if self.is_poe:
            wrong_indices = [i for i in range(len(new_choices)) if i != correct_new_index]
            if not wrong_indices:
                raise ValueError("No wrong choices to select for is_poe=True.")
            final_index = rng.choice(wrong_indices)
        else:
            final_index = correct_new_index

        return new_choices, self._format_answer(answer_fmt, final_index, new_choices)
