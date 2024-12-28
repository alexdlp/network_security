from datetime import datetime
from pathlib import Path
from networksecurity.constants import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp: str = timestamp

        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = Path(self.artifact_name) / timestamp
        


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.data_ingestion_dir:str = Path(training_pipeline_config.artifact_dir) /  training_pipeline.DATA_INGESTION_DIR_NAME
        self.feature_store_file_path:str = Path(self.data_ingestion_dir) /training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR / training_pipeline.FILE_NAME
        self.training_file_path:str = Path(self.data_ingestion_dir) / training_pipeline.DATA_INGESTION_INGESTED_DIR / training_pipeline.TRAIN_FILE_NAME
        self.testing_file_path:str = Path(self.data_ingestion_dir) / training_pipeline.DATA_INGESTION_INGESTED_DIR / training_pipeline.TEST_FILE_NAME

        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str = training_pipeline.DATA_INGESTION_DATABASE_NAME



class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.data_validation_dir = Path(training_pipeline_config.artifact_dir) / training_pipeline.DATA_VALIADTION_DIR_NAME
        self.valid_data_dir: str = Path(self.data_validation_dir) / training_pipeline.DATA_VALIDATION_VALID_DIR
        self.invalid_data_dir: str = Path(self.data_validation_dir) / training_pipeline.DATA_VALIDATION_INVALID_DIR
        self.valid_train_file_path: str = Path(self.valid_data_dir) / training_pipeline.TRAIN_FILE_NAME
        self.valid_test_file_path: str = Path(self.valid_data_dir) / training_pipeline.TEST_FILE_NAME
        self.invalid_train_file_path: str = Path(self.invalid_data_dir) / training_pipeline.TRAIN_FILE_NAME
        self.invalid_test_file_path: str = Path(self.invalid_data_dir)/ training_pipeline.TEST_FILE_NAME
        self.drift_report_file_path: str = Path(self.data_validation_dir) / training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR / training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.data_transformation_dir = Path(training_pipeline_config.artifact_dir) / training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        self.trasformed_train_file_path: str = Path(self.data_transformation_dir) / training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR / training_pipeline.TRAIN_FILE_NAME.replace("csv", "nyp")
        self.transformed_test_file_path: str = Path(self.data_transformation_dir) / training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR / training_pipeline.TEST_FILE_NAME.replace("csv", "nyp")
        self.transformed_objetc_file_path: str = Path(self.data_transformation_dir) / training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR / training_pipeline.PRERPOCESSING_OBJECT_FILE_NAME