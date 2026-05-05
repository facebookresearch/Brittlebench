"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.padding_perturbation import PaddingPerturbation


class TestPaddingPerturbation:

    def test_apply_quotes(self):
        perturbation = PaddingPerturbation(char='\"', char_count=5)
        text = "Another test."
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == '""""" Another test. """""'

    def test_apply_spaces(self):
        perturbation = PaddingPerturbation(char=' ', char_count=5)
        text = "Another test."
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == '      Another test.      '

    def test_apply_new_lines(self):
        perturbation = PaddingPerturbation(char='\n', char_count=3)
        text = "Another test."
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == '\n\n\n Another test. \n\n\n'
