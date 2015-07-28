import os
from fileListGenerator import FileListGenerator
import platform

class FileSystemListGeneratorProvider(FileListGenerator):
	def __init__(self):
		self.paths_to_scan = []

	def prompt_for_paths_to_scan(self):
		default_path = '/'

		if 'windows' in str(platform.system).lower():
			default_path = "C:\\"

		response_default_path = raw_input("Would you like to use the default path for " + platform.system() + " of '" + default_path + "'? [Y/n] ")
		should_use_default = (response_default_path.lower() != 'n')

		if should_use_default:
			self.paths_to_scan = [ default_path ]
			return

		list_of_paths = []

		first_dir = raw_input("Enter first path to scan: ")
		list_of_paths.append(first_dir)

		additional_dir = None

		while additional_dir != '':
			additional_dir = raw_input("Enter additional path to scan (or press enter to continue): ")
			if additional_dir != '':
				list_of_paths.append(additional_dir)

		self.paths_to_scan = list_of_paths

	def get_generator(self):
		list_of_paths = self.paths_to_scan
	
		for base_path in list_of_paths:
			for root,dirs,files in os.walk(base_path):
				for f in files:
					current_file = os.path.join(root,f)
					yield current_file
