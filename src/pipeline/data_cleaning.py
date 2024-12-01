from src.entity.config_entity import DataCleaningConfig
from src.config.configuration import ConfigurationManager
from src.components.data_cleaning import DataCleaning


STAGE_NAME = "Data Cleaning Stage"

class DataCleaningPipeline:
    def __init__(self):
        pass

    def initiate_data_cleaning_pipeline(self):
        try:
            config = ConfigurationManager()
            data_cleaning_config = config.get_data_cleaning_config()
            data_cleaning = DataCleaning(config=data_cleaning_config)
            
            clean_data_path = data_cleaning.initiate_data_cleaning()

            return clean_data_path
        except Exception as e:
            raise e