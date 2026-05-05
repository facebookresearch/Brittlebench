"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.add_space_seq_perturbation import AddSpaceSeqPerturbation

class RewriteAddSpaceSeq(Rewrite):
    """
    Adds random length space sequences in random places in the text based on a probability.

    Args:
        name: The name of the rewrite.
        key: The key in the sample dictionary to apply the perturbation to.
        prob: The probability (0.0 to 1.0) of adding a space sequence after any given character.
        min_spaces: The minimum number of spaces to add (inclusive).
        max_spaces: The maximum number of spaces to add (inclusive).
    """

    def __init__(self,
                 name: str = "rewrite_add_space_seq",
                 key: str = "text",
                 prob: float = 0.1,
                 min_spaces: int = 1,
                 max_spaces: int = 10):
        super().__init__(name=name)
        self.key = key
        self.perturbation = AddSpaceSeqPerturbation(prob=prob, min_spaces=min_spaces, max_spaces=max_spaces)
        self.apply_to = "process_docs"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample
