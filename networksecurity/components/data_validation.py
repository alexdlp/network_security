from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

from networksecurity.utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        
        try: 
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def validate_number_of_colums(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of colums: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            return True if len(dataframe.columns) == number_of_columns else False
   
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold = 0.05)->bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                print(column)
                d1 = base_df[column]
                d2 = current_df[column]

                # Perform the Kolmogorov-Smirnov test
                ks_test_result = ks_2samp(d1, d2)

                is_found = ks_test_result.pvalue < threshold
                if is_found:
                    status = False

                # Update the report with the results
                report[column] = {
                    "p_value": float(ks_test_result.pvalue),
                    "drift_status": str(is_found)
                }

            # Ensure the drift report directory exists
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            drift_report_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the report to a YAML file
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status


        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try: 
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## validate number of columns
            train_status = self.validate_number_of_colums(dataframe=train_dataframe)
            test_status = self.validate_number_of_colums(dataframe=test_dataframe)

          
            ## Data drift
            drift_status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = self.data_validation_config.valid_train_file_path
            dir_path.parent.mkdir(parents=True, exist_ok = True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index = False, header=False)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index = False, header = True)


            if train_status and test_status and drift_status:
                status = True
            else:
                status = False
                
            logging.info(f"Train status: {train_status} | Test status: {test_status} | Drift status: {drift_status}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
