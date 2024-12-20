from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import *

import sys

if __name__ == '__main__':
    try: 

        # load pipeline configuration
        pipeline_config = TrainingPipelineConfig()

        ######## DATA INGESTION #########
        data_ingestion = DataIngestion(DataIngestionConfig(pipeline_config))
        logging.info("Initiate data ingestion")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(data_ingestion_artifact)

        ######## DATA INGESTION #########
        data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
                                         data_validation_config = DataValidationConfig(pipeline_config))
        logging.info("Initiate data validation")

        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

    except NetworkSecurityException as e:
        raise NetworkSecurityException(e, sys)
    

