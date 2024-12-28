import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle

from pathlib import Path

def read_yaml_file(file_path: str) -> dict:
    try: 
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def write_yaml_file(file_path: Path, content: object, replace: bool = False) -> None:
    try:
        path = Path(file_path)
        
        if replace:
            path.unlink(missing_ok=True)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with path.open("w") as file:
            yaml.dump(content, file)
            
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array_data(file_path: Path, data: np.ndarray) -> None:
    """
    Saves a numpy array to the specified file path.

    Args:
        file_path (Path): Path to save the numpy array.
        data (np.ndarray): Data to be saved.

    Raises:
        NetworkSecurityException: If an error occurs during saving.
    """
    try:
        logging.info(f"Saving numpy array data to {file_path}")
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Guardar directamente usando np.save
        np.save(file_path, data)
        logging.info("Numpy array data saved successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_numpy_array_data(file_path: Path) -> np.ndarray:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        
        logging.info(f"Loading numpy array data from {file_path}")
        with open(file_path, "rb") as file:
            return np.load(file_path)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: Path, obj: object) -> None:
    try:
        logging.info(f"Saving object to {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info("Object saved successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path: Path) -> object:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        
        logging.info(f"Loading object from {file_path}")
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e