from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

import sys

if __name__ == '__main__':
    try: 
        data_ingestion = DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
        logging.info("Initiate data ingestion")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except NetworkSecurityException as e:
        raise NetworkSecurityException(e, sys)
    

