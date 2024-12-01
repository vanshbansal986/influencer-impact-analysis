from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataCleaningConfig:
    url_score_data: Path
    clean_data_temp_dir: Path



@dataclass
class ModelTrainingConfig:
    model_name: str
    threshold: float
    distance_metric: str
    output_directory: Path
    model_results_dir: Path


@dataclass
class ResultTransformationConfig:
    influencer_avg_main_dir: Path
    influence_total_score_dir: Path
    urls_score_main_dir: Path
    