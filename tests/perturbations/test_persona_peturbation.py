"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.persona_perturbation import PersonaPerturbation


class TestPersonaPerturbation:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_persona_perturbation(self):
        text = "This is some sample text."

        perturbation = PersonaPerturbation(subset="instruction")

        perturbed_text = perturbation.apply(text)
        assert (
            perturbed_text
            == "You are a film critic specializing in independent and LGBTQ+ cinema, interested in analyzing the representation of queer relationships in modern films.\n\nThis is some sample text."
        )
