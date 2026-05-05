"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re
from brittlebench.perturbations.perturbation import TextPerturbation



class LatexifyPerturbation(TextPerturbation):

    def __init__(self):
        super().__init__()

    def latexify_numbers(self, text):
        # Regex to match in word problems:
        # 1) Dollar amounts like $5 or $5.00
        # 2) Numbers with optional decimals followed by % sign
        # 3) Numbers with units (letters)
        # 4) Standalone numbers
        pattern = re.compile(
            r'(\$\d+(?:\.\d+)?)'          # Dollar amounts
            r'|(\d+(?:\.\d+)?%)'          # Percentages
            r'|(\d+(?:\.\d+)?[a-zA-Z]+)'  # Numbers with units
            r'|(\d+(?:\.\d+)?)'           # Standalone numbers
        )
        
        def replacer(match):
            dollar, percent, unit, standalone = match.groups()
            if dollar:
                # Escape $ inside math mode
                val = dollar.replace('$', r'\$')
                return f"${val}$"
            elif percent:
                # Wrap percentage with escaped %
                number = percent[:-1]
                return f"${number}\\%$"
            elif unit:
                # Separate number and unit, wrap number only
                number_part = re.match(r'\d+(?:\.\d+)?', unit).group(0)
                unit_part = unit[len(number_part):]
                return f"${number_part}$" + unit_part
            elif standalone:
                return f"${standalone}$"
            else:
                return match.group(0)  # fallback, should not happen
        
        return pattern.sub(replacer, text)

    def apply(self, text: str) -> str:
        return self.latexify_numbers(text)



if __name__ == "__main__":
    typo = LatexifyPerturbation()

