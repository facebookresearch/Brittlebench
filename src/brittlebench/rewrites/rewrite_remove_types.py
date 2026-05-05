"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.remove_types_perturbation import RemoveTypesPerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteRemoveTypes(Rewrite):
    """A rewrite that removes type annotations from code snippets."""

    def __init__(self,
                 name: str = "rewrite_remove_types",
                 key: str = "text"):
        super().__init__(name=name)
        self.key = key
        self.perturbation = RemoveTypesPerturbation()
        self.apply_to = "process_docs"
        self.exclusive_tasks = ["humaneval"]


    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(text=sample[self.key])
        return sample
