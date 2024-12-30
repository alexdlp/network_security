import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(DataIngestionConfig(self.training_pipeline_config))
            logging.info("Initiate data ingestion")

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            print(data_ingestion_artifact)

            return data_ingestion_artifact

        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
                                         data_validation_config = DataValidationConfig(self.training_pipeline_config))
            logging.info("Initiate data validation")

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            print(data_validation_artifact)

            return data_validation_artifact

        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_validation_artifact = data_validation_artifact,
                                         data_transformation_config = DataTransformationConfig(self.training_pipeline_config))
            logging.info("Initiate data transformation")

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed")
            print(data_transformation_artifact)

            return data_transformation_artifact
        
        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(data_transformation_artifact = data_transformation_artifact,
                                     model_trainer_config = ModelTrainingConfig(self.training_pipeline_config))
            logging.info("Initiate model training")

            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info("Model training completed")
            print(model_trainer_artifact)

            return model_trainer_artifact
        
        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        

    def sync_artifact_dir_to_s3(self):
        """
        Sync the artifact directory to s3 bucket
        """
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir, 
                                          bucket_name = aws_bucket_url)

        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        
    def sync_saved_model_dir_to_s3(self):
        """
        Sync the final model directory to s3 bucket
        """
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir, 
                                          bucket_name = aws_bucket_url)
        
        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)
        
    def run_training_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            
            return model_trainer_artifact
        
        except NetworkSecurityException as e:
            raise NetworkSecurityException(e, sys)