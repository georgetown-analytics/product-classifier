# apparel.features
# Extracts the features from text for classification and building
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Feb 05 21:15:41 2015 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: features.py [] benjamin@bengfort.com $

"""
Extracts the features from text for classification and building
"""

##########################################################################
## Imports
##########################################################################

import string

from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

##########################################################################
## Featurize Class
##########################################################################

class ProductFeatures(object):
    """
    This class manages the extraction of text features from a product
    document that might contain a name, a description, and keywords. It
    ensures that stopwords and punctuation is excluded, and that all tokens
    are normalized to lower case and to their lemma class (thus reducing
    the feature space for better classification).

    The reason this is a class is because data needs to be stored to do
    the work of featurization - e.g. loading stopwords and punctuation.
    """

    def __init__(self, stoplist=None, punct=None, lemmatizer=None):
        # Load stopwords, punctuation, and lemmatizer
        # This takes a bit of work, so we only want to do it once!
        self.stopwords   = stoplist or stopwords.words('english')
        self.punctuation = punct or string.punctuation
        self.lemmatizer  = lemmatizer or WordNetLemmatizer()

    def tokenize(self, text):
        """
        Returns a list of individual tokens from the text utilizing NLTK's
        tokenize built in utility (far better than split on space). It also
        removes any stopwords and punctuation from the text, as well as
        ensure that every token is normalized.

        For now, token = word as in bag of words (the feature we're using).
        """
        for token in wordpunct_tokenize(text):
            token = self.normalize(token)
            if token in self.punctuation: continue
            if token in self.stopwords: continue
            yield token

    def normalize(self, word):
        """
        Ensures words are in the same class (lemma) as well as lowercase
        """
        word = word.lower()
        return self.lemmatizer.lemmatize(word)

    def featurize(self, name, description=None, keywords=None):
        """
        Returns a dictionary of features to use with the Maximum Entropy
        classifier. In this case we're using a "bag of words" approach.
        """

        # Get the bag of words from the name
        tokens = set(self.tokenize(name))

        # Add the bag of words from the description (union)
        if description is not None:
            tokens = tokens | set(self.tokenize(description))

        # Get the bag of keywords
        keywords = set(self.tokenize(keywords)) if keywords else set([])

        # Create the features
        features = {}
        for token in tokens:
            features[token] = True
        for keyword in keywords:
            features["KEYWORD(%s)" % keyword] = True

        return features

##########################################################################
## Development testing
##########################################################################

if __name__ == '__main__':
    print ProductFeatures().featurize("The Women's EQ Medium Travel Bag from DAKINE. Though it may be small, that does not mean it cannot accomplish great things. The efficient 51 liter interior provides enough space for a week's worth . . .")
