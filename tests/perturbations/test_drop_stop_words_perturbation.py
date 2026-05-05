"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.drop_stop_words_perturbation import DropStopWordsPerturbation

class TestDropStopWordsPerturbation:
    def setup_method(self):
        self.perturbation = DropStopWordsPerturbation()

    def test_apply_removes_stop_words(self):
        input_text = "This is a simple test to check the removal of stop words."
        expected_output = "simple test check removal stop words."
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_handles_empty_string(self):
        input_text = ""
        expected_output = ""
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_no_stop_words(self):
        input_text = "Hello world"
        expected_output = "Hello world"
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_all_stop_words(self):
        input_text = "The is a an it you that"
        expected_output = ""
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_multi_line_text(self):
        input_text = """This is the first line.
                        And this is the second line."""
        expected_output = "first line. second line."
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_with_important_words(self):
        input_text = "who then least less more every in"
        assert self.perturbation.apply(input_text) == input_text

    def test_apply_with_case_sensitive(self):
        input_text = "ABC eV 1234"
        assert self.perturbation.apply(input_text) == input_text
