"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.latexify_perturbation import LatexifyPerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteLatexifyWordProblems(Rewrite):
    """Convert all regular numbers in word problems into LaTeX-formatted numbers"""

    def __init__(self, key: str = "text"):
        super().__init__(name="rewrite_latexify")
        self.key = key
        self.exclusive_tasks = ["gsm8k", "gsm8k_platinum", "gpqa", "mathqa", "aime25"]
        self.perturbation = LatexifyPerturbation()

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample
