"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re

from brittlebench.perturbations.perturbation import TextPerturbation


class SymmetricalOperationPerturbation(TextPerturbation):
    def __init__(self, operation_type="addition"):
        super().__init__()
        if operation_type not in ["addition", "multiplication"]:
            raise ValueError(f"Unsupported operation type: {operation_type}")
        if operation_type == "addition":
            self.symmetric_operation = "(1-1)+"
        elif operation_type == "multiplication":
            self.symmetric_operation = "1*"

    @staticmethod
    def find_math_expressions(text):
        """
        Identifies potential mathematical expressions within a given text and
        returns their (start, end) index spans, including expressions that mix
        numbers and parenthesized sub-expressions (e.g. 2*(3+4)).
        """
        # Treat a parenthesized group as a single operand so outer expressions are captured.
        operand = r'(?:\d+\.?\d*|\.\d+|\([^()]*\))'
        # Full expressions with at least one operator (now allowing parentheses as operands).
        composite_math_pattern = rf'(?:{operand}\s*[\+\-\*\/\^]\s*)+{operand}'
        # Parenthesized expression containing at least one operator (to catch "(3+4)" alone).
        parenthesized_math_pattern = r'\([^()]*[\+\-\*\/\^][^()]*\)'
        # Standalone numbers (kept conditionally by _keep_expression).
        number_pattern = r'\b\d+\.?\d*\b'

        spans = set()

        # Composite expressions (e.g. 2*(3+4), (1+2)*3, 4+(5*6)-7)
        for m in re.finditer(composite_math_pattern, text):
            spans.add((m.start(), m.end()))

        # Parenthesized expressions alone (e.g. (3+4))
        for m in re.finditer(parenthesized_math_pattern, text):
            spans.add((m.start(), m.end()))

        # Numbers
        for m in re.finditer(number_pattern, text):
            spans.add((m.start(), m.end()))

        return sorted(spans, key=lambda t: t[0])

    @staticmethod
    def filter_nested_spans(spans):
        """
        Given a list of (start, end) index spans, filter out those that are nested
        within larger spans, including the ones with the same start or end index.
        """
        if not spans:
            return []

        filtered_spans = []
        current_start, current_end = spans[0]

        for start, end in spans[1:]:
            if start <= current_end:
                # Overlapping or nested span; extend the current_end if needed
                current_end = max(current_end, end)
            else:
                # No overlap; add the current span and move to the next
                filtered_spans.append((current_start, current_end))
                current_start, current_end = start, end

        # Add the last span
        filtered_spans.append((current_start, current_end))
        return filtered_spans

    def apply(self, text):
        # Find all mathematical expressions in the text, return the index spans
        expressions_idxs = self.find_math_expressions(text)

        # Keep only the largest expressions found (avoid nested)
        expressions_idxs = self.filter_nested_spans(expressions_idxs)

        # Apply perturbation by prepending the symmetric operation to each math expression
        offset = 0  # To account for text length changes after insertions
        for start, _ in expressions_idxs:
            start += offset
            text = text[:start] + self.symmetric_operation + text[start:]
            offset += len(self.symmetric_operation)
        return text
