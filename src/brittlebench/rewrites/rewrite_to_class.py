"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.to_class_perturbation import ToClassPerturbation


class RewriteToClass(Rewrite):
    def __init__(self,
                 name: str = "rewrite_to_class",
                 key: str = "text"):
        super().__init__(name=name)
        self.key = key
        self.perturbation = ToClassPerturbation()
        self.exclusive_tasks = ["humaneval"]
        self.apply_to = "process_docs"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample
