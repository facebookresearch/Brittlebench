"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.word_manipulation_perturbation import WordManipulation


class TestWordManipulationPerturbation:
        
    def test_split_words(self):
        perturbation = WordManipulation(manipulation_type="split")
        input_text = "Hello world! This is a test."
        expected_output = "Hel lo world! This is a t est."
        assert perturbation.apply(input_text) == expected_output

    def test_merge_words(self):
        perturbation = WordManipulation(manipulation_type="merge")
        input_text = "Hello world! This is a test."
        expected_output = "Helloworld! This is a test."
        assert perturbation.apply(input_text) == expected_output

    def test_invalid_manipulation_type(self):
        try:
            WordManipulation(manipulation_type="invalid_type")
        except ValueError as e:
            assert str(e) == "Invalid manipulation_type: invalid_type. Must be one of 'split' or 'merge'."
        else:
            assert False, "Expected ValueError for invalid manipulation_type."  
    
    def test_multiline_split(self):
        perturbation = WordManipulation(manipulation_type="split")
        input_text = "Hello world!\nThis is a test."
        expected_output = "H ello world!\nThis is a t est."
        assert perturbation.apply(input_text) == expected_output

    def test_multiline_merge(self):
        perturbation = WordManipulation(manipulation_type="merge")
        input_text = "Hello world!\nThis is a test."
        expected_output = "Helloworld!\nThisis a test."
        assert perturbation.apply(input_text) == expected_output

    def test_no_change_on_empty_string(self):
        perturbation_split = WordManipulation(manipulation_type="split")
        perturbation_merge = WordManipulation(manipulation_type="merge")
        input_text = ""
        assert perturbation_split.apply(input_text) == ""
        assert perturbation_merge.apply(input_text) == ""   
