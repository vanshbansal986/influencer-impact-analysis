from src.constants import *
from src.utils.common import read_yaml , write_yaml , create_directories
from src.entity.config_entity import DataCleaningConfig , ModelTrainingConfig , ResultTransformationConfig

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        
        self.config=read_yaml(config_filepath)


    def get_data_cleaning_config(self)-> DataCleaningConfig:
        
        cleaning_config = self.config.data_cleaning
        
        create_directories([cleaning_config.clean_data_temp_dir])

        data_cleaning_config = DataCleaningConfig(
            url_score_data = cleaning_config.url_score_data,
            clean_data_temp_dir = cleaning_config.clean_data_temp_dir
        )

        return data_cleaning_config


    def get_model_training_config(self)-> ModelTrainingConfig:
        
        training_config = self.config.model_training
    
        
        create_directories([training_config.model_results_dir])

        model_training_config = ModelTrainingConfig(
            model_name = training_config.model_name,
            threshold = training_config.threshold,
            distance_metric = training_config.distance_metric,
            output_directory = training_config.output_directory,
            model_results_dir = training_config.model_results_dir
            
        )

        return model_training_config
    
    def get_result_transformation_config(self)-> ResultTransformationConfig:
        
        transformation_config = self.config.result_transformation
        
        create_directories([transformation_config.influencer_avg_main_dir])
        create_directories([transformation_config.influence_total_score_dir])
        create_directories([transformation_config.urls_score_main_dir])

        result_transformation_config = ResultTransformationConfig(
            influencer_avg_main_dir = transformation_config.influencer_avg_main_dir,
            influence_total_score_dir = transformation_config.influence_total_score_dir,
            urls_score_main_dir = transformation_config.urls_score_main_dir
        )

        return result_transformation_config