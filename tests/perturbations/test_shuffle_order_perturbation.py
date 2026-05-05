"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.shuffle_order_perturbation import ShuffleOrderPerturbation


class TestShuffleOrderPerturbation:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_shuffle_order_perturbation_with_index(self):
        l = ["A", "B", "C"]
        answer = 0

        perturbation = ShuffleOrderPerturbation()

        perturbed_list, updated_answer = perturbation.apply(choices=l,answer=answer)

        assert perturbed_list == ["B", "C", "A"]
        assert updated_answer == 2  # Original answer 0 ("A") is now at index 2

    def test_shuffle_order_perturbation_with_letter(self):
        l = ["A", "B", "C"]
        answer = "A"

        perturbation = ShuffleOrderPerturbation()

        perturbed_list, updated_answer = perturbation.apply(choices=l,answer=answer)

        assert perturbed_list == ["B", "C", "A"]
        assert updated_answer == "C"  # Original answer "A" is now at index 2, which is letter "C"

    def test_shuffle_order_perturbation_with_string(self):
        l = ["choiceA", "choiceB", "choiceC"]
        answer = "choiceA"

        perturbation = ShuffleOrderPerturbation()

        perturbed_list, updated_answer = perturbation.apply(choices=l,answer=answer)

        assert perturbed_list == ["choiceB", "choiceC", "choiceA"]
        assert updated_answer == "choiceA"  # Original answer "choiceA" remains the same

    def test_shuffle_order_perturbation_empty_list(self):
        l = []
        answer = 0

        perturbation = ShuffleOrderPerturbation()

        try:
            perturbation.apply(choices=l,answer=answer)
        except ValueError as e:
            assert str(e) == "Choices list cannot be empty."
        else:
            assert False, "Expected ValueError for empty choices list"

    def test_shuffle_order_perturbation_invalid_index_answer(self):
        l = ["A", "B", "C"]
        answer = 5  # Invalid index

        perturbation = ShuffleOrderPerturbation()

        try:
            perturbation.apply(choices=l,answer=answer)
        except ValueError as e:
            assert str(e) == "Answer index '5' is out of range for choices."
        else:
            assert False, "Expected ValueError for out-of-range index answer"
