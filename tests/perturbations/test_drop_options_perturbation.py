"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

import random
from copy import deepcopy
import pytest

from brittlebench.perturbations.drop_options_perturbation import DropOptionsPerturbation


class TestDropOptionsPerturbation:
    
    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    # Helper: Check if 'sub' is a subsequence of 'seq' (order preserved)
    def _is_subsequence(self, sub, seq):
        it = iter(seq)
        return all(x in it for x in sub)

    def test_drop_options_perturbation_with_index(self):
        options = ["choiceA", "choiceB", "choiceC", "choiceD"]
        orig = deepcopy(options)
        answer = 2  # Correct answer is "choiceC"

        perturbation = DropOptionsPerturbation(target_option_count=2)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["choiceB", "choiceC"]
        assert len(perturbed_options) == 2
        assert set(perturbed_options).issubset(set(options))
        assert self._is_subsequence(perturbed_options, options)
        assert options == orig  # input not mutated
        assert new_answer == 1  # New index of "choiceC" in perturbed list

    def test_drop_options_perturbation_with_text(self):
        options = ["choiceA", "choiceB", "choiceC", "choiceD"]
        orig = deepcopy(options)
        answer = "choiceC"  # Correct answer is "choiceC"

        perturbation = DropOptionsPerturbation(target_option_count=2)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["choiceB", "choiceC"]
        assert len(perturbed_options) == 2
        assert set(perturbed_options).issubset(set(options))
        assert self._is_subsequence(perturbed_options, options)
        assert options == orig  # input not mutated
        assert new_answer == "choiceC"  # New answer text remains the same

    def test_drop_options_perturbation_with_letter(self):
        options = ["choiceA", "choiceB", "choiceC", "choiceD"]
        orig = deepcopy(options)
        answer = "C"  # Correct answer is "choiceC"

        perturbation = DropOptionsPerturbation(target_option_count=2)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["choiceB", "choiceC"]
        assert len(perturbed_options) == 2
        assert set(perturbed_options).issubset(set(options))
        assert self._is_subsequence(perturbed_options, options)
        assert options == orig  # input not mutated
        assert new_answer == "B"  # New letter index of "choiceC" in perturbed list

    def test_drop_options_perturbation_with_poe(self):
        options = ["choiceA", "choiceB", "choiceC", "choiceD"]
        orig = deepcopy(options)
        answer = 2  # Correct answer is "choiceC"

        perturbation = DropOptionsPerturbation(target_option_count=2, is_poe=True)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["choiceB", "choiceC"]
        assert len(perturbed_options) == 2
        assert set(perturbed_options).issubset(set(options))
        assert self._is_subsequence(perturbed_options, options)
        assert options == orig  # input not mutated
        assert new_answer == 0  # New index of "choiceC" in perturbed list

    def test_raises_on_invalid_answer(self):
        options = ["choiceA", "choiceB", "choiceC", "choiceD"]
        perturbation = DropOptionsPerturbation(target_option_count=2)
        with pytest.raises(ValueError):
            perturbation.apply(options, "invalid_choice")

    def test_duplicates_of_correct(self):
        options = ["B", "X", "B", "Y"]
        # correct is the first "B" (index 0)
        perturbation = DropOptionsPerturbation(target_option_count=2)
        perturbed_options, new_answer = perturbation.apply(options, 0)

        # At least one "B" must be present, and order preserved
        assert "B" in perturbed_options
        assert self._is_subsequence(perturbed_options, options)
        assert len(perturbed_options) == 2
        assert new_answer == 0  # New index of "B" in perturbed list

    def test_drop_options_perturbation_no_drop(self):
        options = ["A", "B", "C"]
        answer = 1  # Correct answer is "B"

        perturbation = DropOptionsPerturbation(target_option_count=3)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["A", "B", "C"]  # No options should be dropped
        assert new_answer == 1  # Answer index remains the same

    def test_drop_options_perturbation_excessive_drop(self):
        options = ["A", "B"]
        answer = 0  # Correct answer is "A"

        perturbation = DropOptionsPerturbation(target_option_count=1)
        perturbed_options, new_answer = perturbation.apply(options, answer)

        assert perturbed_options == ["A"]  # Only one option should remain, retaining the correct answer
        assert new_answer == 0  # Answer index remains the same

    def test_drop_options_perturbation_answer_out_of_bounds(self):
        options = ["A", "B", "C"]
        answer = 5  # Invalid index

        perturbation = DropOptionsPerturbation(target_option_count=2)
        with pytest.raises(ValueError):
            perturbation.apply(options, answer)
