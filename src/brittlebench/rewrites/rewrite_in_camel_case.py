"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import ast
from logging import getLogger
from typing import Dict

from brittlebench.perturbations.camel_case_perturbation import CamelCasePerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteInCamelCase(Rewrite):
    """Extract the function def from a code prompt and turn it into camelCase.

    This will also change the function name in the docstring, if it exists.

    Examples:
    "def string_to_md5_foo(text):" -> "def stringToMd5(text):"
    "def generate_integers(a, b):" -> "def generateIntegers(a, b):"
    "def someCamelCaseFunction(x):" -> "def someCamelCaseFunction(x):"
    """

    def __init__(self, 
                 key: str = "text"):
        super().__init__(name="rewrite_in_camel_case")
        self.key = key
        self.exclusive_tasks = ["humaneval"]
        self.apply_to = "process_docs"
        self.perturbation = CamelCasePerturbation()

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample