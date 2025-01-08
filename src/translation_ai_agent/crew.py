from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

# Uncomment the following line to use an example of a custom tool
# from translation_ai_agent.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class TranslationAiAgent():
	"""TranslationAiAgent crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def take_inputs(self, inputs):
		# Set default values for source and target
		default_source = "English"
		default_target = "Chinese"

		# Prompt the user for input values, using default values if input is empty
		source = input(f"Enter the source language (default: {default_source}): ") or default_source
		target = input(f"Enter the target language (default: {default_target}): ") or default_target
		file_path = input("Enter the file_path to translate: ")
		text = ""
		# Open the file and read its content
		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				text = file.read()
				print("File content:\n")
				print(text)
		except FileNotFoundError:
			print(f"The file at {file_path} was not found.")
		except Exception as e:
			print(f"An error occurred: {e}")
		# Assign the inputs to the dictionary
		inputs = {
			'source': source,
			'target': target,
			'text': text
		}

		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def translator(self) -> Agent:
		return Agent(
			config=self.agents_config['translator'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def translation_task(self) -> Task:
		return Task(
			config=self.tasks_config['translation_task'],
		)



	@crew
	def crew(self) -> Crew:
		"""Creates the TranslationAiAgent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
