# src/utils/metadata_manager.py

import json
import logging
import os

class MetadataManager:
    """
    Handles saving and loading metadata for Twitch clips.
    """

    @staticmethod
    def saveMetadata(metadata, filePath):
        """
        Save metadata to a JSON file.

        :param metadata: List of metadata dictionaries to save.
        :param filePath: Path to the JSON file.
        """
        try:
            if os.path.exists(filePath):
                with open(filePath, "r") as file:
                    existingData = json.load(file)
            else:
                existingData = []

            # Append new metadata to existing data
            existingData.extend(metadata)

            # Save back to the file
            with open(filePath, "w") as file:
                json.dump(existingData, file, indent=4)

            logging.info(f"Metadata saved to {filePath}")
        except Exception as e:
            logging.error(f"Error saving metadata: {e}")

    @staticmethod
    def loadMetadata(filePath):
        """
        Load metadata from a JSON file.

        :param filePath: Path to the JSON file.
        :return: List of metadata dictionaries, or an empty list if the file doesn't exist.
        """
        try:
            if os.path.exists(filePath):
                with open(filePath, "r") as file:
                    return json.load(file)
            else:
                logging.warning(f"Metadata file {filePath} not found.")
                return []
        except Exception as e:
            logging.error(f"Error loading metadata: {e}")
            return []
