import sys
import os

from networksecurity.constants.training_pipeline import  TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.entity.config_entity import ModelTrainingConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.utils import save_object, load_object, load_numpy_array_data
from networksecurity.utils.ml_utils import NetworkModel, get_classification_metrics, evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainingConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def train_model(self, X_train, Y_train, X_test, Y_test):
        models = {
            "RandomForest": RandomForestClassifier(verbose=1),
            "DecisionTree": DecisionTreeClassifier(),
            "GradientBoosting": GradientBoostingClassifier(verbose=1),
            "LogisticRegression": LogisticRegression(verbose = 1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "DecisionTree": {
                #"criterion":["gini", "entropy", "log_loss"],
                "criterion":["gini"],
                "max_depth": [5],
                # "splitter": ["best", "random"],
                # "max_features": [ "sqrt", "log2"],
            },
            "RandomForest": {
                #"n_estimators": [8, 16, 32, 64, 128, 256],
                "n_estimators": [256],
                # "criterion": ["gin", "entropy", "log_loss"],
                # "max_depth": 5,
                # "max_features": ["sqrt", "log2"],
            },
            "GradientBoosting": {
                # "loss": ["deviance", "exponential"],
                # "learning_rate": [0.1, 0.05, 0.01, 0.005, 0.001],
                # "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                # "criterion": ["friedman_mse", "mse", "mae"],
                # "max_features": ["sqrt", "log2"],
                # "n_estimators": [16, 32, 64, 128, 256],
                "learning_rate": [0.001],
                "subsample": [0.85],
                "n_estimators": [256],
            },
            "LogisticRegression": {},
            "AdaBoost": {
                # "n_estimators": [8, 16, 32, 64, 128, 256],
                # "learning_rate": [0.1, 0.05, 0.01, 0.005, 0.001],
                "n_estimators": [256],
                "learning_rate": [0.001],
            }
        }

        model_report: dict = evaluate_models(models, params, X_train, Y_train, X_test, Y_test)

        ## Get the  best model score
        best_model_score = max(sorted(model_report.values()))

        ## Get the best model name
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]


        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_metrics(Y_train, y_train_pred)


        ## Tracking in mlflow

        y_test_pred = best_model.predict(X_test)
        classificaion_test_metric = get_classification_metrics(Y_test, y_test_pred)

        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_dir)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor, best_model)
        save_object(self.model_trainer_config.trained_model_dir, Network_Model)
        print("Model saved successfully")
        
        
        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(trained_model_dir=self.model_trainer_config.model_trainer_dir,
                                                      train_metric_artifact=classification_train_metric,
                                                      test_mertric_artifact=classificaion_test_metric)
        
        return model_trainer_artifact





    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            logging.info("Initiating model training")
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]
            )

       
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

       
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
  