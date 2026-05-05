"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.emotion_perturbation import EmotionPerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteEmotionPromptsBase(Rewrite):
    """
    Apply EmotionPrompt on the given question given a specific emoptional stimuli configuration (code).
    Source of prompts: https://llm-enhance.github.io/
    """

    def __init__(self,
                 name: str = "rewrite_emotion_prompt",
                 key: str = "text",
                 stimuli_code: str = "EP01"):
        super().__init__(name=name)
        self.key = key
        self.perturbation = EmotionPerturbation(stimuli_code=stimuli_code)
        self.apply_to = "process_docs"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample


def create_stimuli_class(stimuli_code):
    # Dynamically create the class
    return type(
        f"RewriteEmotionPrompts{stimuli_code}",
        (RewriteEmotionPromptsBase,),
        {
            "__init__": lambda self, key="text": RewriteEmotionPromptsBase.__init__(
                self,
                name=f"rewrite_emotion_prompt_{stimuli_code}".lower(),
                key=key,
                stimuli_code=stimuli_code
            )
        }
    )