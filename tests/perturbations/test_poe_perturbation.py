"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.poe_perturbation import PoEInstructionsPerturbation


class TestPoEInstructionsPerturbation:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_poe_perturbation_positive(self):
        text = "What is the capital of France?\nA. Paris\nB. Madrid\n"

        perturbation = PoEInstructionsPerturbation(is_poe=False)
        perturbed_text = perturbation.apply(text)
        
        assert (
            perturbed_text == ( 
                "Your goal is to identify the correct answer to the multiple choice question.\n"
                "What is the capital of France?\n"
                "A. Paris\n"
                "B. Madrid\n"
                "Correct Answer:"
            )
        )

    def test_poe_perturbation_negative(self):
        text = "What is the capital of France?\nA. Paris\nB. Madrid\n"

        perturbation = PoEInstructionsPerturbation(is_poe=True)
        perturbed_text = perturbation.apply(text)

        assert (
            perturbed_text == (
                "Your goal is to identify the incorrect answer to the multiple choice question.\n"
                "What is the capital of France?\n"
                "A. Paris\n"
                "B. Madrid\n"
                "Incorrect Answer:"
            )
        )

    def test_poe_perturbation_with_answer_suffix(self):
        text_a = "What is the capital of France?\nA. Paris\nB. Madrid\nAnswer:"
        text_b = "What is the capital of France?\nA. Paris\nB. Madrid\nThe answer is:"

        expected_text = ( 
                "Your goal is to identify the correct answer to the multiple choice question.\n"
                "What is the capital of France?\n"
                "A. Paris\n"
                "B. Madrid\n"
                "Correct Answer:"
            )

        perturbation = PoEInstructionsPerturbation(is_poe=False)
        perturbed_text_a = perturbation.apply(text_a)
        perturbed_text_b = perturbation.apply(text_b)
        
        assert perturbed_text_a == expected_text
        assert perturbed_text_b == expected_text
