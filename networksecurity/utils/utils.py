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