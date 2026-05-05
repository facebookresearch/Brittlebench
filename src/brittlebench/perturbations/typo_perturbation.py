"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from augly.text.functional import simulate_typos
from typing import List
from wordfreq import word_frequency
import random
import re

from brittlebench.perturbations.perturbation import TextPerturbation

MEASUREMENT_UNITS = {
    # Time
    "sec", "s", "ms", "us", "ns", "min", "mins", "minute", "minutes",
    "hour", "hours", "hr", "hrs", "second", "seconds",
    "day", "days", "week", "weeks", "year", "years", "month", "months", "Gyr",
    # Length / Distance
    "cm", "cm-1", "cm^-1", "mm", "m", "km", "nm", "fm", "pm", "Angstrom",
    "pc", "kpc", "Mpc", "Gpc", "ly", "AU", "au", "parsecs", "angstrom",
    "meter", "meters", "metre", "metres", "centimeter", "centimeters",
    "kilometer", "kilometers", "inch", "inches", "foot", "feet", "ft",
    "yard", "yards", "mile", "miles",
    # Mass / Weight
    "g", "mg", "ug", "pg", "kg", "amu",
    "gram", "grams", "gm", "pound", "pounds", "lb", "lbs",
    "ounce", "ounces", "oz", "ton", "tons",
    # Energy
    "eV", "keV", "MeV", "GeV", "J", "kJ", "kJ/mol", "kcal", "kcal/mol", "erg",
    # Frequency / Spectroscopy
    "Hz", "MHz", "GHz", "wavenumbers",
    # Pressure
    "Pa", "kPa", "MPa", "bar", "atm",
    # Temperature
    "K", "°C", "°F", "degree", "degrees", "deg", "centigrade", "Kelvin", "kelvin",
    # Volume
    "mL", "ml", "L", "l", "uL", "cc",
    "liter", "liters", "litre", "litres", "gallon", "gallons", "cup", "cups",
    # Area
    "acre", "acres", "sq",
    # Amount / Concentration
    "mol", "mmol", "mole", "moles", "M", "mM", "uM", "nM", "ppm", "g/mol", "g/L",
    "mg/dL", "percent",
    # Velocity / Speed
    "km/s", "m/s", "mph", "kmph", "mps", "kph",
    # Astronomical
    "Msun", "Rsun", "dex",
    # Electrical / Magnetic
    "V", "mV", "kV", "A", "mA", "W", "T", "G", "Tesla", "tesla", "Gauss", "gauss", "H", "F",
    # Radiation
    "Bq", "Ci",
    # Angle
    "rad", "arcsec",
  }


class TypoPerturbation(TextPerturbation):
    """Apply typos only to natural language words, skipping code tokens and symbols.

    Uses the wordfreq library to decide whether a token is a real word. Only
    tokens whose frequency exceeds *min_word_frequency* are perturbed via
    simulate_typos; everything else (identifiers, numbers, punctuation, URLs,
    etc.) is left unchanged.

    Args:
        typo_type: Kind of typo to inject ('charmix', 'keyboard',
            'misspelling', or 'all').
        aug_word_p: Per-word probability of applying a typo.
        aug_char_p: Per-character probability of applying a typo.
        aug_word_min: Minimum number of words to perturb per
            simulate_typos call.
        aug_word_max: Maximum number of words to perturb per
            simulate_typos call.
        language: Language code for wordfreq lookup (default 'en').
        min_word_frequency: Floor frequency. Tokens at or below this
            value are considered non-natural and skipped.  The default
            of 0.0 means any word present in wordfreq's data is eligible.
    """

    def __init__(
        self,
        typo_type: str = "all",
        aug_word_p: float = 0.5,
        aug_char_p: float = 0.5,
        aug_word_min: int = 1,
        aug_word_max: int = 1000,
        language: str = "en",
        min_word_frequency: float = 0.0,
    ):
        super().__init__()

        if typo_type not in ["charmix", "keyboard", "misspelling", "all"]:
            raise ValueError(
                f"Invalid typo_type: {typo_type}. Must be one of "
                "'charmix', 'keyboard', 'misspelling', or 'all'."
            )

        self.typo_type = typo_type
        self.aug_word_p = aug_word_p
        self.aug_char_p = aug_char_p
        self.aug_word_min = aug_word_min
        self.aug_word_max = aug_word_max
        self.language = language
        self.min_word_frequency = min_word_frequency

    def _is_natural_word(self, token: str) -> bool:
        """Return True if *token* is a natural-language word per wordfreq.

        Skips abbreviations (all-caps like "NASA", "GPU") and mixed-case
        tokens that aren't simple title-case or lowercase (e.g. "eV", "pH").
        """
        clean = token.strip(".,!?;:\"'()-[]{}")

        # Skip abbreviations and empty tokens
        if not clean or not clean.isalpha():
            return False

        # Skip measurement units
        if clean in MEASUREMENT_UNITS or clean.lower() in MEASUREMENT_UNITS:
            return False

        # Skip mixed-case tokens that aren't simple title-case or lowercase
        if not (clean.islower() or clean.istitle()):
            return False

        return word_frequency(clean, self.language) > self.min_word_frequency

    def apply(self, text: str) -> str:
        """Apply typos only to natural-language tokens, preserving whitespace."""

        tokens = re.split(r"(\s+)", text)
        natural_indices = [
            i for i, tok in enumerate(tokens)
            if tok and tok.strip() and self._is_natural_word(tok)
        ]
        if not natural_indices:
            return text

        n = len(natural_indices)
        n_perturb = int(round(n * self.aug_word_p))
        n_perturb = max(n_perturb, min(self.aug_word_min, n))
        n_perturb = min(n_perturb, self.aug_word_max, n)

        chosen = set(random.sample(natural_indices, n_perturb))

        for idx in chosen:
            tokens[idx] = simulate_typos(
                [tokens[idx]],
                typo_type=self.typo_type,
                aug_word_p=1.0,
                aug_char_p=self.aug_char_p,
                aug_word_min=1,
                aug_word_max=1,
            )[0]

        return "".join(tokens)


class TypoCountPerturbation(TypoPerturbation):
    """
    Apply a specific number of common typos to a given text.

    Args:
        typo_type: Kind of typo to inject ('charmix', 'keyboard',
            'misspelling', or 'all').
        typos_count: Number of typos to inject.
    """

    def __init__(self,
                 typo_type: str = "all",
                 typos_count: int = 1):
        super().__init__(
            typo_type=typo_type,
            aug_word_p=1.0,
            aug_char_p=1.0,
            aug_word_min=1,
            aug_word_max=1,
        )
        self.typos_count = typos_count

    def apply(self, text: str) -> str:
        """
        Apply exactly `typos_count` typos to the text, preserving whitespace.
        Uses regex tokenization to split on whitespace, perturbing only non-whitespace tokens,
        and then rejoins, preserving all original whitespace (including newlines).
        """
        if not text or self.typos_count < 0:
            return text

        tokens = re.split(r"(\s+)", text)  # keep delimiters (each token is either a word or a sequence of whitespace)
        word_indices = [i for i, tok in enumerate(tokens) if tok and tok.strip() and self._is_natural_word(tok)]
        if not word_indices:  # text has only whitespace
            return text

        typos_count = min(self.typos_count, len(word_indices))
        chosen_indices = random.sample(word_indices, typos_count)
        for idx in chosen_indices:
            tokens[idx] = simulate_typos(
                [tokens[idx]],
                typo_type=self.typo_type,
                aug_word_p=self.aug_word_p,
                aug_char_p=self.aug_char_p,
                aug_word_min=self.aug_word_min,
                aug_word_max=self.aug_word_max,
            )[0]
        return "".join(tokens)


if __name__ == "__main__":
    typo = TypoPerturbation()
