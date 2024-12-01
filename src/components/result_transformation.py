import pandas as pd
import os
import cv2
import numpy as np
from urllib.request import urlretrieve
from imagehash import phash
from PIL import Image
from datetime import datetime
from src import logger
import shutil
from src.entity.config_entity import ResultTransformationConfig

# Directory to store temporary frames



class ResultTransformation:
    def __init__(self , config:ResultTransformationConfig):
        try:
            self.config = config
        except Exception as e:
            raise e
    
    def is_directory_empty(self , directory_path):
        """Check if a directory is empty."""
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            return len(os.listdir(directory_path)) == 0
        else:
            raise FileNotFoundError(f"The directory '{directory_path}' does not exist or is not a directory.")
            

    
    def transform_url_data(self , new_urls_path):
        main_url_dir = self.config.urls_score_main_dir
        
        # If no files exist in the dir , we will just copy the latest clean_url file.
        # This means we are running the pipeline for the first time.
        if self.is_directory_empty(main_url_dir):
            
            destination_file_path = os.path.join(main_url_dir, "clean_data.xlsx")
            logger.info(f"Directory is empty, saving new urls to path: {destination_file_path}")
            shutil.copy(new_urls_path, destination_file_path)
            logger.info(f"File saved at path: {destination_file_path}")

            return destination_file_path
        
        # Data/urls already exist at that path
        else:
            logger.info("Trying to merge existing and current urls data...")
            main_url_dir = self.config.urls_score_main_dir
            main_file_path = os.path.join(main_url_dir , "clean_data.xlsx")
            curr_file_path = new_urls_path
            
            df_main = pd.read_excel(main_file_path)
            df_curr = pd.read_excel(curr_file_path)

            # Concatenate the two DataFrames
            df_combined = pd.concat([df_main, df_curr])

            # Drop duplicates based on the 'URL' column
            df_combined = df_combined.drop_duplicates(subset='url', keep='first').reset_index(drop=True)

            # Save the resulting DataFrame if needed
            df_combined.to_excel(main_file_path)

            logger.info("existing and current urls data merged successfully !!!")

            return main_file_path
    

    def create_and_save_final_inf_data(self , main_total_score_path):

        avg_score_file_dir = self.config.influencer_avg_main_dir
        avg_score_file_path = os.path.join(avg_score_file_dir , "clean_data.xlsx")
        
        logger.info(f"Reading df at path: {main_total_score_path}")
        df = pd.read_excel(main_total_score_path)
        df['avg_score'] = df['total_score']/df['no_of_occurance']
        df = df.sort_values(by='avg_score', ascending=False)

        df.to_excel(avg_score_file_path)
        
        logger.info(f"Final avg data saved to path: {avg_score_file_path}")

        return main_total_score_path
        


    def transform_total_score_data(self , new_inf_total_score_path):
        main_total_score_dir = self.config.influence_total_score_dir
        logger.info(f"Current total score data is at path: {new_inf_total_score_path}")


        # If no files exist in the dir , we will just copy the latest influencer total score file.
        # This means we are running the pipeline for the first time.
        if self.is_directory_empty(main_total_score_dir):
            
            destination_file_path = os.path.join(main_total_score_dir, "clean_data.xlsx")
            
            logger.info(f"Directory is empty, saving new total_score data to path: {destination_file_path}")
            shutil.copy(new_inf_total_score_path, destination_file_path)
            logger.info(f"File saved at path: {destination_file_path}")



            # Saving final results
            return self.create_and_save_final_inf_data(destination_file_path)
        else:
            logger.info("A file for influencer total score data already exists")


            main_total_score_dir = self.config.influence_total_score_dir
            main_total_score_path = os.path.join(main_total_score_dir , "clean_data.xlsx")
            
            curr_total_score_path = new_inf_total_score_path

            logger.info("Combining both new and existing data")
            df_main = pd.read_excel(main_total_score_path)
            df_curr = pd.read_excel(curr_total_score_path)

            # Concatenate the two dataframes
            df_combined = pd.concat([df_main, df_curr])

            # Group by 'hash' and sum 'total_score' and 'no of occurances'
            df_combined = df_combined.groupby('hash', as_index=False).agg({
                'serial_num' : 'first',
                'image_path': 'first',
                'total_score': 'sum',           # Sum scores
                'no_of_occurance': 'sum',       # Keep the first occurrence
                'recent_occurance': 'max'       # Keep the max value

            })

            # Saving the combined dataframe
            df_combined.to_excel(main_total_score_path)
            logger.info(f"Combined data saved to path: {main_total_score_path}")
            

            # Saving final results
            return self.create_and_save_final_inf_data(main_total_score_path)

