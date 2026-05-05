"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.symmetrical_operation_perturbation import SymmetricalOperationPerturbation

class RewriteSymmetricalOperationBase(Rewrite):
    def __init__(self,
                 key: str = "text",
                 name="rewrite_symmetrical_operation",
                 operation_type="addition"):
        super().__init__(name=name)
        self.key = key
        self.apply_to = 'process_docs'

        if operation_type not in ["addition", "multiplication"]:
            raise ValueError(f"Unsupported operation type: {operation_type}")

        self.operation_type = operation_type
        self.exclusive_tasks = ["mathqa", "gsm8k", "gpqa", "aime25"]
        self.perturbation = SymmetricalOperationPerturbation(operation_type=operation_type)

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample

class RewriteSymmetricalAddition(RewriteSymmetricalOperationBase):
    def __init__(self):
        super().__init__(operation_type="addition", name="rewrite_symmetrical_addition")

class RewriteSymmetricalMultiplication(RewriteSymmetricalOperationBase):
    def __init__(self):
        super().__init__(operation_type="multiplication", name="rewrite_symmetrical_multiplication")
