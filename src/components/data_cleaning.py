import pandas as pd
import os
import cv2
import numpy as np
from urllib.request import urlretrieve
from imagehash import phash
from PIL import Image
from datetime import datetime
from src import logger
from src.config.configuration import ConfigurationManager
from src.entity.config_entity import DataCleaningConfig

# Directory to store temporary frames



class DataCleaning:
    def __init__(self,config:DataCleaningConfig):
        self.TEMP_DIR = "temp_frames"
        
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        try:
            self.config = config
        except Exception as e:
            raise e
    
    # Function to download video and capture first few frames
   
    def get_video_frames(self , video_url, frame_count=5):
        
        
        temp_video_path = os.path.join(self.TEMP_DIR, "temp_video.mp4")
        urlretrieve(video_url, temp_video_path)

        cap = cv2.VideoCapture(temp_video_path)
        frames = []
        for _ in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (200, 200))  # Resize for consistent comparison
            frames.append(frame)
        cap.release()
        os.remove(temp_video_path)
        
        return frames
    
  
    def calculate_frame_hashes(self , frames):
        hashes = []
        for frame in frames:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            hashes.append(phash(image))
        return hashes
    
    def initiate_data_cleaning(self):

        excel_data_path = self.config.url_score_data
        
        clean_data_temp_dir = self.config.clean_data_temp_dir

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{current_time}.xlsx"

        clean_data_path = os.path.join(clean_data_temp_dir, filename)

        # Load Excel data
        logger.info(f"Reading excel file at path: {excel_data_path}")
        df = pd.read_excel(excel_data_path)
        #df = df.sample(10)
        logger.info(f"excel file at path: {excel_data_path} read Successfully !!!")
        
        df.rename(columns={'Video URL': 'url'}, inplace=True)

        # Compare videos and retain unique ones
        unique_rows = []  # To store rows corresponding to unique videos
        seen_hashes = set()

        logger.info("Cleaning the URLs...")
        for _, row in df.iterrows():
            url = row['url']
            try:
                frames = self.get_video_frames(url)
                frame_hashes = self.calculate_frame_hashes(frames)

                # If all hashes are new, mark the video as unique
                if not any(frame_hash in seen_hashes for frame_hash in frame_hashes):
                    unique_rows.append(row)  # Store the entire row
                    seen_hashes.update(frame_hashes)
            except Exception as e:
                print(f"Error processing video {url}: {e}")

        # Create a new DataFrame with unique rows
        unique_df = pd.DataFrame(unique_rows)

        logger.info(f"Saving clean data to file : {clean_data_path} ...")
        # Save cleaned data to Excel, retaining all columns
        unique_df.to_excel(clean_data_path, index=False)
        logger.info(f"clean data at path : {clean_data_path} saved successfully !!!")

        

        # Cleanup
        for file in os.listdir(self.TEMP_DIR):
            os.remove(os.path.join(self.TEMP_DIR, file))
        os.rmdir(self.TEMP_DIR)

        return clean_data_path
