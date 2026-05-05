"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from abc import ABC
from typing import List


class TextPerturbation(ABC):
    """Applies a specific perturabtion to a string"""

    def apply(text: str) -> str:
        pass


class ListPerturbation(ABC):
    """Applies a specific perturabtion to list of values, such as shuffling the order."""

    def apply(options: List[str]) -> List[str]:
        pass
