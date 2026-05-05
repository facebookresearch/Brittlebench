"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.perturbations.drop_stop_words_perturbation import DropStopWordsPerturbation

class RewriteDropStopWords(Rewrite):
    """
    Drops common stop words from the text.
    Source: NLTK's English stop words list.
    """

    def __init__(self,
                 name: str = "rewrite_drop_stop_words",
                 key: str = "text"):
        super().__init__(name=name)
        self.key = key
        self.perturbation = DropStopWordsPerturbation()
        self.apply_to = "process_docs"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample
