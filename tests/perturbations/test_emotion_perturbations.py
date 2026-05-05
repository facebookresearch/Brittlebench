"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.emotion_perturbation import EmotionPerturbation


class TestEmotionalPerturbation:

    def test_apply_prefix(self):
        perturbation = EmotionPerturbation(stimuli_code="EP15")
        result = perturbation.apply("This is a question.")
        assert result == "You're safe.\nThis is a question."

    def test_apply_suffix(self):
        perturbation = EmotionPerturbation(stimuli_code="EP03")
        result = perturbation.apply("This is a question.")
        assert result == "This is a question.\nYou'd better be sure."

    def test_default_stimuli(self):
        perturbation = EmotionPerturbation()
        result = perturbation.apply("This is a question.")
        assert result == "This is a question.\nGive me a confidence score between 0-1 for your answer and then write your answer."
