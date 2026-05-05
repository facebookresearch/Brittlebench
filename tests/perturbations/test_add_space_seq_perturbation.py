"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.add_space_seq_perturbation import AddSpaceSeqPerturbation

class TestAddSpaceSeqPerturbation:
    def setup_method(self):
        self.perturbation = AddSpaceSeqPerturbation()
        random.seed(42)

    def test_apply_adds_spaces(self):
        input_text = "This is a test."
        expected_output = "Th     is is a   te    st."
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_handles_empty_string(self):
        input_text = ""
        expected_output = ""
        assert self.perturbation.apply(input_text) == expected_output

    def test_apply_multiple_lines(self):
        input_text = "Hello world.\nThis is a test."
        expected_output = "He     llo wor  ld.    \nThis is a test."
        assert self.perturbation.apply(input_text) == expected_output