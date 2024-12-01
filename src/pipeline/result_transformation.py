from src.entity.config_entity import ResultTransformationConfig
from src.config.configuration import ConfigurationManager
from src.components.result_transformation import ResultTransformation


STAGE_NAME = "Model Training Stage"

class ResultTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self , curr_url_path , curr_inf_avg_score_path):
        try:
            config = ConfigurationManager()
            result_transform_config = config.get_result_transformation_config()
            result_transform = ResultTransformation(config=result_transform_config)

            final_url_path = result_transform.transform_url_data(curr_url_path)
            print(final_url_path)

            final_avg_score_path = result_transform.transform_total_score_data(curr_inf_avg_score_path)
            print(final_avg_score_path)


        except Exception as e:
            raise e