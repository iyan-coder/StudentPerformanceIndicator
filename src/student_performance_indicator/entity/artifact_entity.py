# Artifacts are structured outputs from each stage in the ML pipeline.
# They help track outputs and pass necessary data/configs downstream.
# -------------------------------------------------------------
from dataclasses import (
    dataclass,
)  # Provides a decorator and functions for automatically adding special methods


# ========================================================
# DataIngetionArtifact: Holds paths to split data outputs
# ========================================================
@dataclass  # Simplifies the creation of classes for storing data
class DataIngetionArtifact:
    """
    Artifact class for the data ingestion step.

    Attributes:
        trained_file_path (str): Path to the CSV file containing the training dataset.
        test_file_path (str): Path to the CSV file containing the testing dataset.
    """

    trained_file_path: str  # File path to the training dataset after split
    test_file_path: str  # File path to the testing dataset after split


# ===================================================================
# DataValidationArtifact: Holds output of the data validation process
# ===================================================================
@dataclass
class DataValidationArtifact:
    """
    Artifact class for the data validation step.

    Attributes:
        validation_status (bool): Indicates if the validation was successful (True/False).
        valid_train_file_path (str): Path to the validated training dataset.
        valid_test_file_path (str): Path to the validated testing dataset.
        invalid_train_file_path (str): Path to the invalid training dataset, if any.
        invalid_test_file_path (str): Path to the invalid testing dataset, if any.
        drift_report_file_path (str): Path to the saved data drift report (YAML).
    """

    validation_status: bool  #  Was validation successful or not
    valid_train_file_path: str  #  Path to valid training data
    valid_test_file_path: str  #  Path to valid testing data
    invalid_train_file_path: str  #  Path to invalid training data (if validation fails)
    invalid_test_file_path: str  #  Path to invalid testing data (if validation fails)
    drift_report_file_path: str  #  Path to YAML file storing the drift detection report


@dataclass
class DataTransformationArtifact:
    """
    Data class for storing artifact paths generated during the data transformation step
    of a machine learning pipeline.

    Attributes:
        transformed_object_file_path (str): Path to the serialized preprocessing object
                                            (e.g., imputer, scaler, encoder).
        transformed_train_file_path (str): Path to the preprocessed and transformed training dataset.
        transformed_test_file_path (str): Path to the preprocessed and transformed testing dataset.
        feature_columns_file_path (str): Path to the saved list of feature column names (as .pkl).
    """

    # File path to the serialized preprocessing object (e.g., imputer, scaler, encoder)
    transformed_object_file_path: str

    # File path to the transformed training dataset (after preprocessing)
    transformed_train_file_path: str

    # File path to the transformed testing dataset (after preprocessing)
    transformed_test_file_path: str

    feature_columns_file_path: str


# ===================================================================================
# RegressionMetricArtifact: Data class to store key regression evaluation metrics
# ===================================================================================
@dataclass
class RegressionMetricArtifact:
    # R² (Coefficient of Determination) - measures how well predictions approximate actual values
    r2_score: float

    # RMSE (Root Mean Squared Error) - penalizes large errors more than MAE
    root_mean_squared_error: float

    # MAE (Mean Absolute Error) - measures average absolute difference between predictions and true values
    mean_absolute_error: float


# =========================================================================
# ModelTrainerArtifact: Data class to encapsulate the outcome of model training
# =========================================================================
@dataclass
class ModelTrainerArtifact:
    # File path where the trained model (pickle or similar) is saved for later use
    trained_model_file_path: str

    # Classification metrics evaluated on the training dataset to check model fit
    train_metric_artifact: RegressionMetricArtifact

    # Classification metrics evaluated on the test dataset to check generalization
    test_metric_artifact: RegressionMetricArtifact
