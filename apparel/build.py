# apparel.build
# Builds classifier models and saves them as pickles
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Feb 05 21:11:27 2015 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: build.py [] benjamin@bengfort.com $

"""
Builds classifier models and saves them as pickles
"""

##########################################################################
## Imports
##########################################################################

import os
import time
import json
import pickle
import random
import apparel
import unicodecsv as csv

from datetime import datetime
from apparel.config import settings
from apparel.features import ProductFeatures
from nltk.classify.util import accuracy
from nltk.classify import MaxentClassifier

##########################################################################
## Module Constants
##########################################################################

DATE_FORMAT = "%a %b %d %H:%M:%S %Y"

##########################################################################
## Model Builder
##########################################################################

class ClassifierBuilder(object):
    """
    Creates a classifier model using MaximumEntropy and saves it as a
    pickle to disk. This class also writes out extra information to disk
    to ensure that the model can be identified in the future.
    """

    def __init__(self, corpus=None, **kwargs):
        self.corpus      = corpus or settings.corpus
        self.validate    = kwargs.pop('validate', True)    # Perform cross validation
        self.outpath     = kwargs.pop('outpath', '.')      # Where to write out the data

        # Compute info and model paths
        self.model_path, self.info_path = self.get_output_paths()

        # Other required properties
        self.accuracy    = None  # Accuracy of the model
        self.started     = None  # Start timestamp of the build
        self.finished    = None  # Finish timestamp of the build
        self.buildtime   = None  # Time (seconds) of complete build
        self.feattime    = None  # Time (seconds) to get features
        self.traintime   = None  # Time (seconds) to train the model
        self.validtime   = None  # Time (seconds) to run the validation

        # Create a featurizer
        self.featurizer  = ProductFeatures()

        # Cache the features on the model
        self._featureset = None

    def featureset(self):
        """
        Opens the corpus path, reads the data and constructs features to
        pass to the classifier. (A simple improvement is to cache this).

        Returns a dictionary of features and the label as follows:

            [(feats, label) for row in corpus]

        This is the expected format for the MaxentClassifier.
        """

        if self._featureset is None:

            # Time how long it takes to extract features
            start = time.time()

            self._featureset = []
            with open(self.corpus, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    label = row.pop('category')
                    feats = self.featurizer.featurize(**row)
                    self._featureset.append((feats, label))

            # Record feature extraction time
            self.feattime = time.time() - start

        return self._featureset

    def train(self, featureset=None):
        """
        Trains the maximum entropy classifier and returns it. If a
        featureset is specified it trains on that, otherwise it trains on
        the models featureset.

        Pass in a featureset during cross validation.
        Returns the training time and the classifier.
        """
        featureset = featureset or self.featureset()

        # Time how long it takes to train
        start = time.time()

        classifier = MaxentClassifier.train(featureset,
                        algorithm='megam', trace=1, gaussian_prior_sigma=1)

        delta = time.time() - start
        return classifier, delta

    def build(self):
        """
        Builds the model and writes to the outpath (which should be a
        directory). Two files are written:

            - the pickle of the model
            - a yaml file of associated data

        Note, if a file already exists at the outpath, this will raise an
        exception (don't want to overwrite a model by accident!)
        """

        # Record the start time
        self.started  = datetime.now()
        start = time.time()

        # Extract the features and train the model
        classifier, self.traintime = self.train()

        # Write the classifier to disk
        with open(self.model_path, 'w') as f:
            pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)

        # Begin accuracy validation
        if self.validate:
            self.cross_validate()

        # Record the finish time
        self.finished = datetime.now()
        self.buildtime = time.time() - start

        # Write the information to disk
        self.write_details()

    def cross_validate(self):
        """
        Performs cross validation by training the model on 90% of the
        corpus then checking the accuracy on the remaining 10%.
        """
        start  = time.time()

        feats  = self.featureset()
        offset = len(feats) / 10
        random.shuffle(feats)

        train  = feats[:offset]
        test   = feats[offset:]

        classifier, _  = self.train(train)
        self.accuracy  = accuracy(classifier, test)

        self.validtime = time.time() - start

    def get_output_paths(self):
        """
        Returns two paths - the pickle path and the information yaml path.
        Ensures those paths don't exist and wont' be overwritten.
        """

        today = datetime.now().strftime('%Y-%d-%m')
        mname = os.path.join(self.outpath, "model-%s.pickle" % today)
        iname = os.path.join(self.outpath, "info-%s.json" % today)

        for name in (mname, iname):
            if os.path.exists(name):
                raise Exception("Can't overwrite file at '%s'!" % name)

        return mname, iname

    def write_details(self):
        """
        Writes the details of the classifier to a YAML file.
        """

        details = {
            'version': apparel.get_version(),
            'started': self.started.strftime(DATE_FORMAT),
            'finished': self.finished.strftime(DATE_FORMAT),
            'accuracy': self.accuracy,
            'validated': self.validate,
            'corpus': self.corpus,
            'paths': {
                'model': self.model_path,
                'info': self.info_path,
            },
            'classes': {
                'classifier': MaxentClassifier.__name__,
                'features': ProductFeatures.__name__,
            },
            'timer': {
                'build': self.buildtime,
                'features': self.feattime,
                'validation': self.validtime,
                'training': self.traintime,
            }
        }

        with open(self.info_path, 'w') as f:
            json.dump(details, f, indent=4)

if __name__ == '__main__':
    builder = ClassifierBuilder()
    print builder.build()
