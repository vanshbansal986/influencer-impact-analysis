from src.entity.config_entity import ModelTrainingConfig
from src.config.configuration import ConfigurationManager
from src.components.model_training import ModelTraining


STAGE_NAME = "Model Training Stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_training_pipeline(self , clean_data_path):
        try:
            config = ConfigurationManager()
            model_training_config = config.get_model_training_config()
            model_training = ModelTraining(config=model_training_config , clean_data_path = clean_data_path)
            
            final_data_path = model_training.initiate_model_training()
            print(f"final_data_path : {final_data_path}")

            return final_data_path
        except Exception as e:
            raise e