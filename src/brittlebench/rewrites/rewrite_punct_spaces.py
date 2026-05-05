"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict
 
from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.punct_spaces_perturbation import PunctSpacesPerturbation


class RewritePunctSpaces(Rewrite):
    """
    Adds a pair of whitespaces around each punctuation mark.
    Source: https://arxiv.org/abs/2503.11751
    """

    def __init__(self,
                 name: str = "rewrite_punct_spaces",
                 key: str = "text"):
        super().__init__(name=name)
        self.key = key
        self.perturbation = PunctSpacesPerturbation()
        self.apply_to = "process_docs"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample
