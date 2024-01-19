import numpy as np
import pandas as pd


class LinearRegressor():
    """
    Ordinary Least Squares Linear Regressor

    LinearRegressor will fit a linear model with coefficients w = (w1, w2, ..., wn)
    to minimize Residual Sum of Squares (RSS) between the observed targets values
    in the dataset, and the targets predicted by the linear approximation for the
    examples in the dataset.
    """
    def __init__(self):
        self.coef = None
        pass

    def fit(self, X, y):
        """
        Fits the linear model according to the OLS mechanism.

        Parameters
        ----------
        X : {array-like matrix} of shape (n_examples, n_features)
            Dataset that will be used as the feature values to train the model.

        y : array-like matrix of shape (n_examples, n_targets)
            Dataset that will be used as the target values to train the model.

        Returns
        -------
        self : object
            Fitted Estimator.
        """
        # X_np = np.array(X)
        # self.coef = np.linalg.inv(X_np.T @ X_np) @ X_np.T @ y
        # return self
        X_np = np.array(X)
        y_np = np.array(y)

        # Check if dimensions of both matrices are correct
        if X_np.ndim != 2:
            raise ValueError("X should be a 2D array.")
        if y_np.ndim != 1:
            raise ValueError("y should be a 1D array.")

        # Check if the number of samples in X and y match
        if X_np.shape[0] != y_np.shape[0]:
            raise ValueError("The number of examples in X and y should be equal.")

        if X_np.shape[0] < X_np.shape[1]:
            raise ValueError("The number of examples in X should be greater than the number of features.")

        
        self.coef = np.linalg.inv(X_np.T @ X_np) @ X_np.T @ y_np
        return self.coef

    def predict(self, X):
        """
        Predicts target values using the fitted linear model.
        
        Parameters
        ----------
        X : array-like matrix of shape (n_samples, n_features)
            Feature values that will be used to make predictions.
        
        Returns
        -------
        predictions : array-like matrix of shape (n_samples, n_targets)
            Predicted target values for the input feature values.
        """
        if self.coef is None:
            raise ValueError("Model not fitted. Call fit first.")

        X = np.array(X)

        # Check if dimensions of X are correct
        if X.ndim != 2:
            raise ValueError("X should be a 2D array.")

        # Check if the number of features in X equals to the number of coefficients
        if X.shape[1] != len(self.coef):
            raise ValueError("The number of features in X should be equal to the number of coefficients.")
        
        # Check if non-numeric values exist in input
        if not np.issubdtype(X.dtype, np.number):
            raise ValueError("Input contains non-numeric values.")
            
        # Check if NaN values exist in input
        if np.isnan(X).any():
            raise ValueError("Input contains NaN values.")
        
        # check if infinite values exist in input
        if not np.isfinite(X).all():
            raise ValueError("Input contains infinite values.")

        pred = X @ self.coef
        return pred

    def score(self, df, true_column, pred_column):
        """
            Calculates the coefficient of determination R^2 for the prediction.

            Parameters
            ----------
            y_true : array-like matrix, shape (n_samples, n_targets)
            True target values.

            y_pred : array-like matrix, shape (n_samples, n_targets)
            Predicted target values.

            Returns
            -------
            r2_score : float
                Coefficient of determination R^2.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        if df.empty or len(df) < 2:
            raise ValueError("DataFrame must have at least two data points")

        y_true = df[true_column].values
        y_pred = df[pred_column].values

        #  Calculate mean value of y_true
        y_true_mean = np.mean(y_true)

        # Calculat（SST）
        SST = np.sum((y_true - y_true_mean) ** 2)

        # Calculate（SSE）
        SSE = np.sum((y_true - y_pred) ** 2)

        # Calculate R^2
        r2 = 1 - (SSE / SST)

        return r2

