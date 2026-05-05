"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import string 
import re

from brittlebench.perturbations.perturbation import TextPerturbation


class PunctSpacesPerturbation(TextPerturbation):
    """
    Add a pair of whitespaces around each punctuation mark.
    Perturbation present in: https://arxiv.org/abs/2503.11751
    """

    def __init__(self):
        super().__init__()

    def apply(self, text: str) -> str:
        """
        Adds a space before and after punctuation, unless it's at a boundary.
        This preserves existing spacing and newlines.
        """
        # Create a regex pattern to match punctuation.
        punct_set = re.escape(string.punctuation)
        
        # Pattern: a non-space character (`[^\s]`) followed by a punctuation character.
        text = re.sub(r'([^\s])([' + punct_set + r'])', r'\1 \2', text)
        
        # Pattern: a punctuation character followed by a non-space character.
        text = re.sub(r'([' + punct_set + r'])([^\s])', r'\1 \2', text)
        
        return text
