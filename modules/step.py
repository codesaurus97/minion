"""
Parent Interface object for pipeline steps
"""

import os
import subprocess
import click
import minion.config as config


class Step(object):
    """
    Interface class for defining a pipeline step.

    Attributes
    ----------
    name: str
        Name of the pipeline step
    type: str
        Type of the pipeline step
    """

    name: str = "" # Name of the pipeline step
    type: str = "" # Type of the pipeline step
    __status: int= 1 # Status code of the current step

    def __init__(self, yaml_dict: dict):
        """
        Create a pipeline step based on a yaml dictionary.
        
        Parameters
        ----------
        yaml_dict : dict
            YAML dictionary to parse (part of a yaml file)
        
        Raises
        ------
        NotImplementedError
            The function has to be implemented in subclasses
        """
        raise NotImplementedError

    @property
    def status(self) -> int:
        """
        Get the execution status of the pipeline step
        
        Returns
        -------
        int
            Return code of the terminal command
        """
        return self.__status
    
    def _setstatus(self, status:int):
        """
        Set the execution status of the step after execution
        
        Parameters
        ----------
        status : int
            Returned execution result code from the command
        """
        self.__status = status

    def execute(self) -> bool:
        """
        Execute the current pipeline step and return the result.
        
        Returns
        -------
        bool
            True = Execution successful; False= Execution error
        
        Raises
        ------
        NotImplementedError
            The function has to be implemented in subclasses
        """
        raise NotImplementedError


class DefaultStep(Step):

    cmd: str = "" # Command string to execute
    args: list = None

    def __init__(self, yaml_dict: dict):
        self.name = yaml_dict['name']
        self.type = yaml_dict['type']
        self.cmd  = yaml_dict['cmd']
        self.args = yaml_dict['args']
    
    def execute(self) -> int:
        """
        Execute the command with the default type handler (`os.system()`)
        
        Returns
        -------
        int
            Return code of the command execution
        
        Note
        ----
        The given commands are executed via the subprocess modules
        """
        cmdarray = [self.cmd]
        cmdarray.extend(self.args)

        # Print the command 
        click.echo(config.SHELLCHAR + " " + " ".join(cmdarray))

        try:
            p = subprocess.Popen(cmdarray, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (child_stdin, child_stdout, child_stderr) = (p.stdin, p.stdout, p.stderr)

            # Set the returncode to 0, when no exception happened
            self._setstatus(0)
        except subprocess.CalledProcessError as cmderror:
            self._setstatus(cmderror.returncode)

        output = child_stdout.read().decode('utf-8')

        # Print the command results
        click.echo(output)

        return self.status


def create(yaml_dict: dict) -> Step:
    """
    Create a pipeline step object from the yaml dictionary. The creation uses the Factory
    pattern to create an interface typed object from the given representation
    
    Parameters
    ----------
    `yaml_dict` : dict
        YAML dictionary of the pipeline step
    
    Returns
    -------
    Step
        Pipeline step as the Step interface
    """
    if yaml_dict['type'] == 'default':
        return DefaultStep(yaml_dict)
    else:
        raise ValueError("The pipeline type is not available!") 