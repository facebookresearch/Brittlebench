"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from nltk.corpus import stopwords
import re
import nltk

from brittlebench.perturbations.perturbation import TextPerturbation

nltk.download('stopwords')

IMPORTANT_WORDS = {
    # question words
    'who', 'what', 'where', 'when', 'why', 'how', 'which',
    # negation
    'not', 'no', 'nor', 'don\'t', 'doesn\'t', 'didn\'t', 'haven\'t', 'aren\'t', 'isn\'t', 'hasn\'t',
    # math related words
    'each', 'every', 'per', 'at', 'least', 'most', 'exactly', 'y',
    # logic
    'if', 'then', 'before', 'after', 'when',
    # time / space
    'between', 'into', 'over', 'under', 'before', 'after', 'during', 'without', 'in', 'on',
    # comparisons
    'more', 'less', 'most', 'least', 'many', 'few', 'all', 'some'
}


class DropStopWordsPerturbation(TextPerturbation):
    """Drops common stop words from the text."""

    def __init__(self):
        super().__init__()

    def apply(self, text):
        """Removes articles and common stop words from an input text."""
        if text is None:
            return ""

        # 1. Get the comprehensive English stop words list from NLTK
        # This list includes 'a', 'an', 'the', 'is', 'in', 'it', 'you', 'that', etc.
        stop_words = set(stopwords.words('english')) - IMPORTANT_WORDS

        # 2. Filter out the stop words
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # 3. Rejoin words and normalize whitespace
        cleaned_text = ' '.join(filtered_words)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text
