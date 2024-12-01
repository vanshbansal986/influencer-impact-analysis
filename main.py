from src.pipeline.data_cleaning import DataCleaningPipeline 
from src.pipeline.model_training import ModelTrainingPipeline 
from src.pipeline.result_transformation import ResultTransformationPipeline
from src import logger



if __name__ == '__main__':
    try:
        
        STAGE_NAME = "Data Cleaning Stage"
        
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataCleaningPipeline()
        clean_url_data_path = obj.initiate_data_cleaning_pipeline()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        
        STAGE_NAME = "Model Training Stage"
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        clean_inf_avg_data_path = obj.initiate_model_training_pipeline(clean_url_data_path)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")


        STAGE_NAME = "Data Tranformation Stage"
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ResultTransformationPipeline()
        inf_avg_data_path = obj.initiate_data_transformation(clean_url_data_path , clean_inf_avg_data_path)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e
    