"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict

from brittlebench.perturbations.persona_perturbation import PersonaPerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewritePersonaBase(Rewrite):
    """Apply irrelevant personas to a given sample key.
    Source of personas: https://huggingface.co/datasets/proj-persona/PersonaHub
    """

    def __init__(self, key: str = "text", name="", subset=""):
        super().__init__(name=name)
        self.key = key
        self.perturbation = PersonaPerturbation(subset=subset)
        self.apply_to = "build_all_requests"

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample


class RewritePersonaInstruction(RewritePersonaBase):
    def __init__(self, key: str = "text"):
        super().__init__(key, name="rewrite_persona_instruction", subset="instruction")


class RewritePersonaKnowledge(RewritePersonaBase):
    def __init__(self, key: str = "text"):
        super().__init__(key, name="rewrite_persona_knowledge", subset="knowledge")


class RewritePersonaMath(RewritePersonaBase):
    def __init__(self, key: str = "text"):
        super().__init__(key, name="rewrite_persona_math", subset="math")
