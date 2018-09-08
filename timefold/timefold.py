import numpy as np

class timefold(object):
    """
    Cross-validation methods for timeseries data.

    Available methods
        * nested
            Generates train-test pair indices with a growing training window.

            Example (folds=3):
            TRAIN: [0 1 2] TEST: [3 4 5]
            TRAIN: [0 1 2 3 4 5] TEST: [6 7 8]
            TRAIN: [0 1 2 3 4 5 6 7] TEST: [8 9]

        * window
            Generates train-test pair indices with a moving window.

            Example (folds=3):
            TRAIN: [0 1 2] TEST: [3 4 5]
            TRAIN: [3 4 5] TEST: [6 7 8]
            TRAIN: [6 7] TEST: [8 9]

        * step
            Generates one step ahead train-test pair indices with specified testing size.

            Fold argument is ignored. The maximum possible number of folds is generated based on
            the number of samples and specified testing window size.

            Example (test_size=1):
            TRAIN: [0] TEST: [1]
            TRAIN: [0 1] TEST: [2]
            TRAIN: [0 1 2] TEST: [3]
            TRAIN: [0 1 2 3] TEST: [4]
            TRAIN: [0 1 2 3 4] TEST: [5]
            TRAIN: [0 1 2 3 4 5] TEST: [6]
            TRAIN: [0 1 2 3 4 5 6] TEST: [7]
            TRAIN: [0 1 2 3 4 5 6 7] TEST: [8]
            TRAIN: [0 1 2 3 4 5 6 7 8] TEST: [9]

        * shrink
            Generates train-test pair indices with a shrinking training window and constant testing window.

            Example (folds=3):
            TRAIN: [0 1 2 3 4 5 6 7] TEST: [8 9]
            TRAIN: [3 4 5 6 7] TEST: [8 9]
            TRAIN: [6 7] TEST: [8 9]

        * stratified
            Generates stratified train-test pair indices where a ratio is preserved per fold.

            To be implemented
    """

    def __init__(self, folds=10, method='nested', test_size=1):
        self.folds = folds
        self.method = method
        self.test_size = test_size

    def split(self, X):
        """
        Split data into train-test pairs based on specified cross-validation method.
        """
        folds = self.folds
        method = self.method
        test_size = self.test_size

        X_obs = X.shape[0]
        indices = np.arange(X_obs)

        if folds >= X_obs:
            raise ValueError(
                ("The number of folds {0} must be smaller than the number of observations {1}".format(folds, X_obs)))

        folds += 1
        fold_indices = np.array_split(indices, folds, axis=0)
        fold_sizes = [len(fold) for fold in fold_indices][:-1]
        train_starts = [fold[0] for fold in fold_indices][:-1]
        train_ends = [fold[0] for fold in fold_indices][1:]

        if method == 'nested':
            for end, size in zip(train_ends, fold_sizes):
                yield(indices[:end], indices[end:end + size])

        elif method == 'window':
            for start, end, size in zip(train_starts, train_ends, fold_sizes):
                yield(indices[start:end], indices[end:end + size])

        elif method == 'step':
            steps = indices[1:]
            for step in steps:
                yield(indices[:step], indices[step:step + test_size])

        elif method == 'shrink':
            for start, size in zip(train_starts, fold_sizes):
                yield(indices[start:train_ends[-1]], indices[-fold_sizes[-1]:])

        elif method == 'stratified':
            pass

        else:
            raise ValueError("Unknown method supplied '{0}'. Method must be one of: 'nested', 'window', 'step', "
                             "'stratified'".format(method))
