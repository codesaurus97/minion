import click
import os
import minion.config as config
from tabulate import tabulate
from minion.modules.banana import find_banana
from minion.modules.target import Target, parse_target, JobNotFoundError

@click.group()
def cli():
    """
    Minion command automation framework written in python.
    """
    pass

@cli.command()
@click.argument('path', required=False)
def list(path: str = None):
    """
    List the defined minion jobs in the selected path.
    """
    if path is None:
        path = '.'

    try:
        # Find the banana configuraiton file to execute
        banana_yaml = find_banana(path)

        # Parse the banana target
        target = parse_target(banana_yaml=banana_yaml)

        try:
            tbllist = []
            # List the available jobs
            for each_job in target.jobs:
                tbllist.append((each_job.name, each_job.desc))
            
            print(tabulate(tbllist, ('Job', 'Description'), tablefmt="simple"))

        except JobNotFoundError as exc:
            click.secho(str(exc), fg='red')

    except FileNotFoundError as exc:
        # The banana configuration is not found
        click.secho(str(exc), fg='red')

@cli.command()
@click.argument('path', required=True)
@click.argument('job', required=False)
def run(path: str, job: str):
    """
    Execute a job, which is defined in the banana.yaml configuration file.
    
    PATH - Path of the directory to look for the banana
    JOB  - Name of the job to run
    """

    if path is None:
        path = '.'

    try:
        # Find the banana configuraiton file to execute
        banana_yaml = find_banana(path)

        # Parse the banana target
        target = parse_target(banana_yaml=banana_yaml)

        try:
            target.execute(job=job)
        except JobNotFoundError as exc:
            click.secho(str(exc), fg='red')

    except FileNotFoundError as exc:
        # The banana configuration is not found
        click.secho(str(exc), fg='red')


if __name__ == '__main__':
    cli()
    