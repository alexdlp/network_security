import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


from networksecurity.constants.training_pipeline import  TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.utils import save_object, save_numpy_array_data

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def get_data_transformer_object(cls)-> Pipeline:
        """
        Initialises KNNImputer object with the parameters defined in the training_pipeline.py file
        and returns a pipeline object with the imputer object"""
        try:
            logging.info("Creating data transformer object")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            return Pipeline(steps = [("imputer", imputer)])
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training dataframe
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN], axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## testid dataframe
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN], axis = 1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            ## imputer
            preprocessor = self.get_data_transformer_object()
            preprocessor.fit(input_feature_train_df)

            transformed_input_feature_train_df = preprocessor.transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_feature_train_df, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test_df, np.array(target_feature_test_df)]

            # save transformed data
            save_numpy_array_data(self.data_transformation_config.trasformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_objetc_file_path, preprocessor)

            # prepare artifacts

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.trasformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path = self.data_transformation_config.transformed_objetc_file_path
            )

            logging.info("Data transformation completed")

            return data_transformation_artifact



        except Exception as e:
            raise NetworkSecurityException(e, sys)  

