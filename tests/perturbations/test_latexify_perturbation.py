"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.latexify_perturbation import LatexifyPerturbation


class TestLatexifyPerturbation:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_latexify_perturbation(self):
        text = "Aleena subscribed to a streaming service that charges her $140 per month. If the streaming company charged her the initial amount for the first half of the year and then charged her 10% less money on the other half of the year, calculate the total amount she had paid for the streaming service by the end of the year."

        perturbation = LatexifyPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Aleena subscribed to a streaming service that charges her $\\$140$ per month. If the streaming company charged her the initial amount for the first half of the year and then charged her $10\\%$ less money on the other half of the year, calculate the total amount she had paid for the streaming service by the end of the year."

    def test_latexify_perturbation_no_numbers(self):
        text = "The quick brown fox jumps over the lazy dog."

        perturbation = LatexifyPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == text

    def test_latexify_number_at_the_end_of_seq(self):
        text = "The total cost is $50."

        perturbation = LatexifyPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "The total cost is $\\$50$."
