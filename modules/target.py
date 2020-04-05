import minion.modules.step as step
import minion.modules.job as job
import yaml
import click

class JobNotFoundError(Exception):
	pass

class Target(object):
	"""
	Target class for build target functionalities.
	"""
	
	name: str  = "" # Name of the target (build-nane)
	desc: str  = "" # Description of the target
	os: list   = None # List of operating systems
	glob: dict = None # List of global variables in the target
	jobs: list = None # List of pipeline steps

	def __init__(self, yaml_dict: dict):
		"""
		Create a new target from a parsed yaml dictionary.
		
		Parameters
		----------
		yaml_dict : dict
			Parsed YAML dictionary from .yaml file.
		"""
		
		# Parse the mandatory parameters
		self.name = yaml_dict['name']
		self.desc = yaml_dict['desc']
		self.os   = yaml_dict['os']
		self.glob = yaml_dict['glob']

		self.jobs = []
		
		# TODO: Verify unique job names
		for each_job in yaml_dict['jobs']:
			jobname = each_job
			jobyaml = yaml_dict['jobs'][jobname]
			self.jobs.append(job.create(jobname, jobyaml))

	def execute(self, job: str):
		"""
		Execute the selected minion job in banana.yaml
		
		Parameters
		----------
		job : str
			Name of the job to execute. jog='all' will execute all available jobs
		"""

		if job == 'all':
			click.secho('Running \'all\' jobs...')
			click.echo()

			# Execute all jobs
			for each_job in self.jobs:
				each_job.execute()
		else:
			job_flt = filter(lambda j: j.name == job, self.jobs)
			list_jobs = list(job_flt)

			if(len(list_jobs)) < 1:
				raise JobNotFoundError("The job {job} is not found.".format(job=job))
			else:
				click.secho('Running job \'{job}\'...'.format(job=job))
				click.echo()

				# Execute the selected job
				list_jobs[0].execute()

def parse_target(banana_yaml: str) -> Target:
	"""
	Parse the target configuration from the yaml string. All jobs and all steps will be
	parsed accordingly. If any of these steps leads to an error, the parsing will be stopped.
	
	Parameters
	----------
	banana_yaml : str
		String representation of the banana.yaml file
	
	Returns
	-------
	Target
		Target object
	"""
	# Parse the YAML to dict
	yaml_dict = yaml.load(banana_yaml, Loader=yaml.FullLoader)

	# We do the replacement here...
	glob = yaml_dict['glob']

	for each_glob in glob:
		yaml_processed = banana_yaml.replace('{{%s}}' % each_glob, yaml_dict['glob'][each_glob])

	# Reload with the replaced global values
	yaml_dict = yaml.load(yaml_processed, Loader=yaml.FullLoader)

	return Target(yaml_dict)