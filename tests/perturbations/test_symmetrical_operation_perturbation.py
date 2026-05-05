"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.symmetrical_operation_perturbation import SymmetricalOperationPerturbation
import re


class TestSymmetricalOperationPerturbation:
    
    def test_addition(self):
        text = "Calculate (2 + 3) * 5 and also consider 10 / 2 - 1. Then this: 7 is just a number. Also this: (4)." \
        " Finally, check 3.14 * (1 + 2)."
        expected_text = "Calculate (1-1)+(2 + 3) * 5 and also consider (1-1)+10 / 2 - 1. Then this: (1-1)+7 is just a number. Also this: ((1-1)+4). Finally, check (1-1)+3.14 * (1 + 2)."

        perturbation = SymmetricalOperationPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == expected_text

    def test_multiplication(self):
        text = "Calculate (2 + 3) * 5 and also consider 10 / 2 - 1. Then this: 7 is just a number. Also this: (4)." \
        " Finally, check 3.14 * (1 + 2)."
        expected_text = "Calculate 1*(2 + 3) * 5 and also consider 1*10 / 2 - 1. Then this: 1*7 is just a number. Also this: (1*4). Finally, check 1*3.14 * (1 + 2)."   
        perturbation = SymmetricalOperationPerturbation(operation_type="multiplication")
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == expected_text

    def test_unsupported_operation(self):
        try:
            SymmetricalOperationPerturbation(operation_type="subtraction")
        except ValueError as e:
            assert str(e) == "Unsupported operation type: subtraction"
        else:
            assert False, "Expected ValueError for unsupported operation type"

    def test_no_math_expressions(self):
        text = "This is a simple sentence without any math."
        expected_text = text

        perturbation = SymmetricalOperationPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == expected_text
