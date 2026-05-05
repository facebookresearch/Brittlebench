"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.shuffle_choices_perturbation import ShuffleChoicesPerturbation


class TestShuffleChoicesPerturbation:
    
    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_shuffle_choices_perturbation_letter_format(self):
        text = ( 
            "What is the capital of France?\n"
            "A. Paris\n"
            "B. London\n"
            "C. Athens\n"
            "Answer:"
        )
        perturbation = ShuffleChoicesPerturbation()
        shuffled = perturbation.apply(text)
        assert shuffled != text
        assert "A. Paris" in shuffled
        assert "B. London" in shuffled
        assert "C. Athens" in shuffled


    def test_shuffle_choices_perturbation_number_format(self):
        text = ( 
            "What is the capital of France?\n"
            "1. Paris\n"
            "2. London\n"
            "3. Athens\n"
            "Answer:"
        )
        perturbation = ShuffleChoicesPerturbation()
        shuffled = perturbation.apply(text)

        assert shuffled != text
        assert "1. Paris" in shuffled
        assert "2. London" in shuffled
        assert "3. Athens" in shuffled

    def test_shuffle_choices_perturbation_parenthesis_numbers(self):
        text = ( 
            "What is the capital of France?\n"
            "1) Paris\n"
            "2) London\n"
            "3) Athens\n"
            "Answer:"
        )
        perturbation = ShuffleChoicesPerturbation()
        shuffled = perturbation.apply(text)

        assert shuffled != text
        assert "1) Paris" in shuffled
        assert "2) London" in shuffled
        assert "3) Athens" in shuffled


    def test_shuffle_choices_perturbation_parenthesis_letters(self):
        text = ( 
            "What is the capital of France?\n"
            "A) Paris\n"
            "B) London\n"
            "C) Athens\n"
            "Answer:"
        )
        perturbation = ShuffleChoicesPerturbation()
        shuffled = perturbation.apply(text)

        assert shuffled != text
        assert "A) Paris" in shuffled
        assert "B) London" in shuffled
        assert "C) Athens" in shuffled
