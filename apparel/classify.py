# apparel.classify
# Classifier package - utilize built model to perform classifications
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Feb 05 21:43:21 2015 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: classify.py [] benjamin@bengfort.com $

"""
Classifier package - utilize built model to perform classifications
"""

##########################################################################
## Imports
##########################################################################

import pickle

from operator import itemgetter
from apparel.config import settings
from apparel.features import ProductFeatures

##########################################################################
## Simple Classifier
##########################################################################

class ApparelClassifier(object):
    """
    Performs classification of products using a classifier that is loaded
    via a pickle at runtime. This classifier can be of any type, but we
    expect the Maximum Entropy classifier trained from a CSV corpus.
    """

    def __init__(self, model=None):
        """
        Pass in the path of the pickle classifier object.
        """

        ## Get the default model from the settings if it isn't passed in
        model = model or settings.model

        ## Load the model from the pickle
        with open(model, 'rb') as pkl:
            self._classifier = pickle.load(pkl)

        ## Create a featurizer to use
        self.featurizer = ProductFeatures()

    def classify(self, name, description=None, keywords=None):
        """
        Classifies the text using the internal classifier. Returns a
        probability distribution of the labels associated with the text.
        """
        features = self.featurizer.featurize(name, description, keywords)
        probdist = self._classifier.prob_classify(features)
        labels   = [(label, probdist.prob(label))
                    for label in probdist.samples()
                    if probdist.prob(label) > 0.01]
        return sorted(labels, key=itemgetter(1), reverse=True)

    def explain(self, name, description=None, keywords=None):
        """
        Wrapper for classifier.explain - prints out (no way to capture the
        string output, unfortunately) the features contributing to the
        chosen classifier.
        """
        features = self.featurizer.featurize(name, description, keywords)
        self._classifier.explain(features)

    def labels(self):
        """
        Wrapper for classifier.labels - returns a list of the labels.
        """
        return self._classifier.labels()

if __name__ == '__main__':
    classifier = ApparelClassifier()
    classifier.explain("GUESS Handbag, Isla Large Satchel")
