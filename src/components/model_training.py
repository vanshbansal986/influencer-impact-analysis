from src import logger
import os
import cv2
import tempfile
from deepface import DeepFace
from urllib.request import urlopen
import shutil
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance
import pandas as pd
from src import logger
from datetime import datetime
from src.entity.config_entity import ModelTrainingConfig
from src.config.configuration import ConfigurationManager


class ModelTraining:
    def __init__(self , config:ModelTrainingConfig , clean_data_path):
        try:
            self.config = config
            self.clean_data_path = clean_data_path

            columns = ['image_path', 'hash', 'total_score', 'no_of_occurance' , 'recent_occurance']
            # Create an empty DataFrame with the specified columns
            df = pd.DataFrame(columns=columns)

            self.df = df

        except Exception as e:
            raise e


    def handle_unique(self , output_directory , face_path  , j , model_name , distance_metric , score):
        
        """
        Handles the faces that are unique by creating a new row for unique image.
        This is done by extracting the hash using deepface.find() of the face image
        
        Args:
            output_directory (str): returned by deepface.find() function.
            face_path(str) : Path of the current unique face
            j (int): Current video number which we are iterating
            
        
        Returns:
            None: Just updates the df
        """
        
        df = self.df
        
        logger.info("Adding unique image in the dataframe...")
    
        # Finding hash of image
        hash = DeepFace.find(
                img_path=face_path,
                db_path=output_directory,
                model_name=model_name,
                threshold = 0.8,
                distance_metric=distance_metric
            )[0].iloc[0]['hash']
        
        
        # Creating new row
        new_row = {
            'image_path' : face_path,
            'hash' : hash,
            'total_score' : score,
            'no_of_occurance' : 1,
            'recent_occurance': j
        }
    
        # Update the DataFrame i.e add the new row
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        self.df = df
        logger.info(f"New row for unique image added successfully !!! \n {new_row} ")
    
    
    def handle_not_unique(self , results  , score , j):
        """
        Handles the faces that are not unique by updating the score for most similar image.
        This is done by extracting the hash of the most similar image from the results datatype.
    
        
        Args:
            results: res
            output_directory (str): returned by deepface.find() function.
            score (int): perfomance score of the current video
            j (int): Current video number which we are iterating
            
        
        Returns:
            None: Just updates the df
        """
    
        df = self.df
    
        # if df.loc[df['hash'] == hash, 'j'] == j and df.loc[df['hash'] == hash, 'unique_face_num'] == unique_face_count:
        #     return
        
        hash = results[0].iloc[0]['hash']
    
        logger.info(f"Handling Duplicate image with hash: {hash} and j: {j}")
    
        if df.loc[df['hash'] == hash, 'recent_occurance'].iloc[0] == j:
            logger.info("This face has already occured in this video")
            return
    
        
        # Update the 'score' and 'no_of_occurances' aswell as 'recent_occurance'  of the row where 'hash' is hash
        df.loc[df['hash'] == hash, 'total_score'] += score
        df.loc[df['hash'] == hash, 'no_of_occurance'] += 1
        df.loc[df['hash'] == hash, 'recent_occurance'] = j
        
        self.df = df
        logger.info("Duplicate image row has been updated !!!")
        
    
    
    def process_video_frames(self ,frame_directory,j, metric , output_directory="unique_faces", 
                             model_name="Facenet", 
                             distance_metric="cosine", 
                             max_unique_faces = 4,
                             threshold=0.6):
        """
        Process frames from a directory to extract and store unique faces using DeepFace as well as update the df.
        
        Args:
            frame_directory (str): Path to directory containing video frames
            output_directory (str): Path to store unique faces
            model_name (str): Face recognition model to use
            distance_metric (str): Metric for face comparison
            threshold (float): Similarity threshold for unique face detection
        """
        # Create directories
        os.makedirs(output_directory, exist_ok=True)
        os.makedirs("temp_unique_faces", exist_ok=True)
    
        # Track unique faces
        unique_faces_count = 0
    
        logger.info(f"Processing video frames of video: {j}")
    
        frame_num = 1
        # Iterate through frames
        for frame_filename in sorted(os.listdir(frame_directory)):
            if frame_filename.endswith(('.jpg', '.png', '.jpeg')):
                frame_path = os.path.join(frame_directory, frame_filename)
                
                try:
                    # Detect faces using DeepFace
                    detections = DeepFace.extract_faces(
                        frame_path, 
                        detector_backend="mtcnn", 
                        enforce_detection=True,
                        align=True
                    )
                    
                    logger.info(f"Found faces in frame {frame_num} of video {j}")
        
                    # Process each detected face
                    for i, detection in enumerate(detections):
                        if unique_faces_count >= max_unique_faces:
                            return
                        
                        # Extract the face
                        if detection['confidence'] > 0.95:
                            logger.info("Face is clear")
                            face = detection['face']
                        else:
                            logger.info("Face is not clear")
                            continue
                        
                        # Ensure face is valid
                        if face is None or face.size == 0:
                            print(f"Invalid face detected in {frame_filename}")
                            continue
                        
                        # Convert to uint8 if needed
                        if face.dtype != np.uint8:
                            face = (255 * face).astype(np.uint8)
                        
                        # Convert to PIL Image
                        pil_face = Image.fromarray(face)
                        
                        # Enhance face image
                        enhanced_face = self.enhance_face_image(pil_face)
                        
                        # Temporary path for current face
                        temp_face_path = os.path.join("temp_unique_faces", f"temp_face.jpg")
                        enhanced_face.save(temp_face_path)
    
                        
                        # Check if the face is unique
                        logger.info("Checking if the face is unique...")
                        is_unique , results = self.check_unique_face(
                            temp_face_path, 
                            output_directory, 
                            model_name, 
                            distance_metric, 
                            threshold
                        )
                        
                        # Save unique face
                        if is_unique:
                            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            unique_filename = f"unique_face_{current_time}.jpg"
                            unique_path = os.path.join(output_directory, unique_filename)
    
                            logger.info(f"face is unique and saving it to {unique_path}")
                            
                            # Save enhance face image
                            enhanced_face.save(unique_path)
                            unique_faces_count += 1
    
                            # Call the function to update the df
                            score = metric[j-1]
                            self.handle_unique(output_directory , unique_path , j , model_name , distance_metric , score)
    
                        else:
                            # Face is not unique and already exists
                            logger.info("face is not unique")
                            
                            score = metric[j-1]
                            if results is not None:
                                
                                # Call the function to update the df
                                logger.info("result variable is not none and calling the handle_not_unique function")
                                self.handle_not_unique(results , score , j)
                    
    
                    frame_num += 1
                except Exception as e:
                    logger.info(f"No face in this frame {frame_num} of video {j}")
    
    def check_unique_face(self , face_path, output_directory, model_name, distance_metric, threshold):
        """
        Check if the face is unique compared to existing faces in the output directory
        
        Args:
            face_path (str): Path to the current face image
            output_directory (str): Directory containing existing unique faces
            model_name (str): Face recognition model
            distance_metric (str): Metric for face comparison
            threshold (float): Similarity threshold
        
        Returns:
            bool: True if face is unique, False otherwise
        """
        # If output directory is empty, face is unique
        if not os.listdir(output_directory):
            logger.info("Directory is empty so face is unique")
            return True , None
        
        try:
            # Use DeepFace to find similar faces
            results = DeepFace.find(
                img_path=face_path,
                db_path=output_directory,
                model_name=model_name,
                threshold = 0.8,
                distance_metric=distance_metric
            )
            
            # Check if any similar faces are found
            if results is None or (isinstance(results, pd.DataFrame) and results.empty):
                logger.info("No similar faces found in directory so face is unique")
                return True , None
            
            # If results exist, check the distance
            if isinstance(results, list) and len(results) > 0:
                # Get the minimum distance
                logger.info("Checking the distance of existing faces in dir")
                min_distance = results[0]['distance'].min() if not results[0].empty else float('inf')
                
                return min_distance > threshold , (None if min_distance > threshold else results)
            
    
            logger.info("similar faces found in directory so face is not unique")
            return False , results
        
        except ValueError as e:
            # If an error occurs (e.g., no faces found), consider it not unique since it likely does not contain a face
            logger.info("No faces found in image or some other error so we are not considering it unique ")
            return False , None
    
    
    
    def enhance_face_image(self , pil_image, resize_dim=(256, 256)):
        """
        Enhance face image quality
        
        Args:
            pil_image (PIL.Image): Input face image
            resize_dim (tuple): Target resize dimensions
        
        Returns:
            PIL.Image: Enhanced face image
        """
        # Resize image
        resized_image = pil_image.resize(resize_dim, Image.LANCZOS)
        
        # Enhance sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(resized_image)
        sharpened_image = sharpness_enhancer.enhance(2.0)
        
        # Enhance contrast
        contrast_enhancer = ImageEnhance.Contrast(sharpened_image)
        enhanced_image = contrast_enhancer.enhance(1.2)
        
        return enhanced_image
    
    # Function to create the main directory for storing unique faces
    def create_main_directory(self , directory="unique_faces"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    
    # Function to create/clear the extracted frames directory
    def create_extracted_frames_directory(self , directory="extracted_frames"):
        if os.path.exists(directory):
            shutil.rmtree(directory)  # Remove existing frames
        os.makedirs(directory)
        return directory
    
    # Function to extract frames from a video
    def extract_frames(self ,video_path, frame_count=20):
        frames = []
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(total_frames // frame_count, 1)  # Calculate frame interval
        
        for i in range(frame_count):
            frame_index = i * interval
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        cap.release()
        return frames
    # Function to process videos and extract unique faces
    def process_videos(self , video_urls, metric , main_dir="unique_faces", frame_count=30, model_name="Facenet", distance_metric="cosine", threshold=0.4):
        main_dir = self.create_main_directory(main_dir)
        
        # Iterate over each video URL
        j = 1
        for video_url in video_urls:
            logger.info(f"Processing video: {video_url}")
            print(f"Processing video: {video_url}")
    
            # Create/clear the extracted frames directory for each video
            extracted_frames_dir = self.create_extracted_frames_directory("extracted_frames")
            
            # Download the video to a temporary file
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video:
                temp_video.write(urlopen(video_url).read())
                temp_video.flush()
    
                # Extract frames from the video
                frames = self.extract_frames(temp_video.name, frame_count=frame_count)
                
                # Store extracted frames temporarily in the extracted_frames directory
                for frame_index, frame in enumerate(frames):
                    frame_path = os.path.join(extracted_frames_dir, f"frame_{frame_index}.jpg")
                    cv2.imwrite(frame_path, frame)
                
                # Iterate through extracted frames to detect faces and store unique faces
                self.process_video_frames(extracted_frames_dir, j , metric)
                
                # Clean up the extracted frames directory after processing
                shutil.rmtree(extracted_frames_dir)
                j += 1
    
        print("Processing completed.")
    
    def initiate_model_training(self):

        final_data_dir = self.config.model_results_dir

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{current_time}.xlsx"

        final_data_path = os.path.join(final_data_dir, filename)


        df = pd.read_excel(self.clean_data_path)

        
        # List of video URLs
        video_urls = df['url'].to_list()
        metric = df['Performance'].to_list()
        
        # Run the process
        self.process_videos(video_urls , metric)
        
        self.df.index.name = 'serial_num'

        self.df = self.df.sort_values(by='total_score', ascending=False)

        self.df.to_excel(final_data_path)

        return final_data_path
    