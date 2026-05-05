"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re
import random

from typing import Optional
from brittlebench.perturbations.perturbation import TextPerturbation


class ShuffleChoicesPerturbation(TextPerturbation):
    """
    Shuffle the order of multiple choice options in a prompt.
    """
    def __init__(self, seed: Optional[int] = None):
        super().__init__()
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def apply(self, text: str) -> str:
        # Regex pattern to match option labels at start of line:
        # Supports: A. B) 1. 2) i. ii) I) II) a: b:
        option_label_re = re.compile(
        r"^\s*(?:[A-Za-z]|\d+|[IVXLCDMivxlcdm]{1,7})\s*([.) :])\s*",
        re.MULTILINE,
        )
        # Locate the 'Answer:' line (case-insensitive), if present
        answer_match = re.search(r"^\s*Answer\s*:", text, re.MULTILINE | re.IGNORECASE)
        answer_pos = answer_match.start() if answer_match else len(text)
        # Find option label starts only before the 'Answer:' section
        matches = [m for m in option_label_re.finditer(text) if m.start() < answer_pos]
        # If fewer than 2 options, do nothing
        if len(matches) < 2:
            return text
        # Compute the exact slices for each option block
        starts = [m.start() for m in matches]
        blocks = []
        for i, s in enumerate(starts):
            e = starts[i + 1] if i + 1 < len(starts) else answer_pos
            blocks.append(text[s:e])
        # Shuffle the blocks with reproducibility if seed provided
        rng = random.Random(text)
        shuffled = blocks[:]
        rng.shuffle(shuffled)
        # Rebuild the full prompt:
        # - Everything before the first option stays
        # - Then the shuffled options
        # - Everything from the end of the last option (answer_pos) to the end stays
        prefix = text[:starts[0]]
        suffix = text[answer_pos:]  # includes 'Answer:' onward if present
        return prefix + "".join(shuffled) + suffix