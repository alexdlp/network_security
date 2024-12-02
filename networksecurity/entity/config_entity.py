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