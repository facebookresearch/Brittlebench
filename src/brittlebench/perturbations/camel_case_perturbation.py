"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from caseconverter import camelcase
import re

from brittlebench.perturbations.perturbation import TextPerturbation


class CamelCasePerturbation(TextPerturbation):
    """Convert a string in snake_case to camelCase, leaving the first character unchanged.

    Examples:
    "apply_edit" -> "applyEdit"
    "convert_to_camel_case" -> "convertToCamelCase"
    """

    @staticmethod
    def _find_variable_names_in_text(text: str) -> set[str]:
        pattern = r'\b[\w_]*_[\w_]*\b'
        matches = re.findall(pattern, text)
        return set(matches)

    def apply(self, text: str) -> str:
        variable_names = self._find_variable_names_in_text(text)
        for var_name in variable_names:
            text = text.replace(var_name, camelcase(var_name))
        return text
