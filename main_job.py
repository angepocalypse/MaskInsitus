import requests
import tempfile
import os
import time
from urllib.parse import urlparse

from mask_insitu import overlay_images
from search_wiki_commonsV2 import search_wiki_commons


class InsituMakerJob:

    # Example usage
    BACKGROUND_PATH = 'img/pexels-karolina-grabowska-4207891_1080.png'
    MASK_PATH = 'img/pexels-karolina-grabowska-4207891_1080_mask.png'
    FOREGROUND_PATH = 'img/tame_impala_bleed_11x14.jpg'
    OUTPUT_PATH = 'output'

    TMP_DIRECTORY = 'tmp'

    ART_LIST = []

    '''
    Class for handling all of the image and metadata for a piece of art
    '''
    def __init__(self):
        print("Initialized InsituMakerJob")

    @staticmethod
    def download_image(image_url, folder_path, retry_attempts=3, retry_delay=2):
        filename = os.path.basename(image_url)
        file_path = os.path.join(folder_path, filename)

        headers = {'User-Agent': 'InsituMaker/0.0'}

        for attempt in range(retry_attempts):
            try:
                response = requests.get(image_url, stream=True, headers=headers)
                response.raise_for_status()

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print("Image downloaded successfully:", file_path)
                return file_path  # Exit the function if the image is downloaded successfully

            except Exception as e:
                print("Error occurred while downloading image:", e)

                if attempt < retry_attempts - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Maximum retry attempts reached. Failed to download image.")

        return  # Exit the function if all retry attempts fail
    
    @staticmethod
    def make_filesystem_friendly(string):
        # Define a translation table to remove specific characters
        translation_table = str.maketrans("", "", ':\\')

        # Apply the translation table to remove the characters from the string
        filesystem_friendly_string = string.translate(translation_table)
        if "File" in filesystem_friendly_string: 
            filesystem_friendly_string = filesystem_friendly_string.split("File")[1]
        return filesystem_friendly_string.split(".")[0]
    
    def initialize_paths(self):
        if not os.path.exists(self.TMP_DIRECTORY):
            os.makedirs(self.TMP_DIRECTORY)
        if not os.path.exists(self.OUTPUT_PATH):
            os.makedirs(self.OUTPUT_PATH)


    def start(self):
        print("Starting main job")
        self.initialize_paths()
        # Example usage
        search_query = "Van Gogh paintings"
        print(f"Querying wiki commons for {search_query}")
        self.ART_LIST = search_wiki_commons(search_query, max_results=6)
        
        for art_work in self.ART_LIST:
            # if not art_work.is_portrait():
            #     print(f"Skipping artwork {art_work.title} because it is landscape")
            #     continue
            print(f"Attempting to download art_work {art_work.title}")
            tmp_filepath = self.download_image(art_work.thumb_url,
                                               self. TMP_DIRECTORY,
                                               retry_attempts=3, 
                                               retry_delay=2)
            friendly_name = self.make_filesystem_friendly(art_work.title)
            output_name = friendly_name + "_thumbnail.jpg"
            out_path = os.path.join(self.OUTPUT_PATH, output_name)
            print(f"Overlaying {friendly_name} with tmp path {tmp_filepath} at path {out_path}")
            overlay_images(self.BACKGROUND_PATH,
                           self.MASK_PATH,
                           tmp_filepath, 
                           out_path)

if __name__ == "__main__":
    insituMakerJob = InsituMakerJob()
    insituMakerJob.start()
