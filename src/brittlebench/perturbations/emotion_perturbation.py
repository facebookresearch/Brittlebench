"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.perturbation import TextPerturbation

import json
import os

stimuli_path = os.path.join(os.path.dirname(__file__), 'resources', 'emotion_prompts.json')
with open(stimuli_path, 'r') as f:
    EMOTION_PROMPTS = json.load(f)


class EmotionPerturbation(TextPerturbation):
    """
    EmotionPerturbation applies emotional prompts (stimuli) to a given text by either prefixing or suffixing
    the text with a specified emotional prompt.

    Attributes:
        stimuli_code (str): The code of the emotional prompt (stimuli) to be applied.

    Methods:
        apply(text: str) -> str:
            Applies the selected emotion prompt (stimuli) to the input text, either as a prefix or suffix,
            depending on the stimuli type defined in EMOTION_PROMPTS.
    """

    def __init__(self, stimuli_code: str = "EP01"):
        super().__init__()
        self.stimuli_code = stimuli_code

    def apply(self, text: str) -> str:
        prompt = EMOTION_PROMPTS[self.stimuli_code]
        if prompt['type'] == 'prefix':
            return prompt['text'] + '\n' + text
        elif prompt['type'] == 'suffix':
            return text + '\n' + prompt['text']
        else:
            raise NotImplementedError(f"Unknown prompt type {prompt['type']}")
