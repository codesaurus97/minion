"""
Module for finding banana configuration files automatically.
"""

import os
import minion.config as config

def find_banana(path: str) -> str:
    """
    Find the banana.yaml in the given directory and read it's contents.
    
    Parameters
    ----------
    path : str
        Path to search
    
    Returns
    -------
    str
        Contents of the banana.yaml file
    
    Raises
    ------
    FileNotFoundError
        The given path is not valid
    FileNotFoundError
        The given path does not contain a banana.yaml file
    """
    if os.path.exists(path) and os.path.isdir(path):
        bananapath = os.path.join(path, config.BANANA_FILENAME)

        if os.path.exists(bananapath) and os.path.isfile(bananapath):
            
            with open(bananapath, 'r') as fp:
                bananafile = fp.read()
                return bananafile
        else:
            raise FileNotFoundError("There is no build configuration to be found. Please create a banana.yaml file.")
    else:
        raise FileNotFoundError("The given path is not valid!")