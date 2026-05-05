"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.punct_spaces_perturbation import PunctSpacesPerturbation


class TestPuncSpacesPerturbation:

    def test_punc_spaces_perturbation(self):
        text = "Hello, world! This is a test."
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "Hello , world ! This is a test ."

    def test_punc_spaces_perturbation_no_punctuation(self):
        text = "Hello world This is a test"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == text

    def test_punc_spaces_perturbation_multiple_punctuation(self):
        text = "Wait... What?! Really???"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "Wait . . . What ? ! Really ? ? ?"

    def test_punc_spaces_perturbation_edge_case(self):
        text = "!!!...,,,"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "! ! ! . . . , , ,"

    def test_punc_spaces_perturbation_leading_trailing(self):
        text = "... Hello, world!!!"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == ". . . Hello , world ! ! !"
    
    def test_punc_spaces_perturbation_mixed(self):
        text = "Hello... Are you sure? Yes, I'm sure!"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "Hello . . . Are you sure ? Yes , I ' m sure !"
    
    def test_punc_spaces_perturbation_empty_string(self):
        text = ""
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == text

    def test_punc_spaces_perturbation_only_spaces(self):
        text = "     "
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == text

    def test_punc_spaces_perturbation_preserving_spaces(self):
        text = "   Hello, beautiful   world!   "
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "   Hello , beautiful   world !   "

    def test_punc_spaces_perturbation_preserving_new_lines(self):
        text = "\n   Hello, world!\n   This is a test.\n\n"
        perturbation = PunctSpacesPerturbation()
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == "\n   Hello , world !\n   This is a test .\n\n"
