"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.padding_perturbation import PaddingPerturbation


AVAILABLE_CHARS = {'spaces': ' ', 'quotes': '\"', 'new_lines': '\n'}


class RewritePaddingPromptBase(Rewrite):
    def __init__(self,
                 name: str = "rewrite_padding_prompt",
                 key: str = "text",
                 char_count: int = 10,
                 char: str = ""):
        super().__init__(name=name)
        self.key = key
        self.perturbation = PaddingPerturbation(char=char, char_count=char_count)
        self.apply_to = "build_all_requests"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample


def create_padding_prompt_class(char, char_count):
    if char not in AVAILABLE_CHARS:
        raise ValueError(f"Character '{char}' is not supported. Choose from {list(AVAILABLE_CHARS.keys())}.")
    
    # Dynamically create the class
    return type(
        f"RewritePaddingPrompt{char}{char_count}",
        (RewritePaddingPromptBase,),
        {
            "__init__": lambda self, key="text": RewritePaddingPromptBase.__init__(
                self,
                name=f"rewrite_{char}_{char_count}".lower(),
                key=key,
                char_count=char_count,
                char=AVAILABLE_CHARS[char]
            )
        }
    )
