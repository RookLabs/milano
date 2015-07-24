import time


class ResultsWriter(object):
	def __init__(self, logger):
		self.logger = logger


	def write_results(self, results):
		output = self.get_output(results)
		self.write_results_to_file(output)
		self.write_results_to_terminal(output)


	def get_output(self, results):
		output = 'Scan date: ' + time.strftime("%c") + \
			'\n' + \
			'Scan duration (seconds): ' + str(results.scan_time_seconds) + \
			'\n\n' + \
			'Files requiring review as they match Hacking Team MD5 signatures\n' + \
			'  Category (A=Detected via VirusTotal  B=Detected via manual analysis\n' + \
			'            C=From malicious project   D=Undetermined)\n' + \
			'-----------------------------------------------------------------------------------\n'

		if len(results.detected_file_paths) > 0:
			for path in results.detected_file_paths:
				output += path.potential_category + ': ' + path.file_path + '\n'
		else:
			output += 'No files found that require review\n'

		return output


	def write_results_to_terminal(self, output):
		self.logger.info('\n\n')
		self.logger.info(output)


	def write_results_to_file(self, output):
		f = open('last_scan_results.txt','w')

		f.write(output + '\n')

		f.close()


class Results(object):
	def __init__(self):
		self.detected_file_paths = []
		self.scan_time_seconds = 0


	def start(self):
		self.start_time = time.time()
		time.clock()


	def finish(self):
		self.scan_time_seconds = time.time() - self.start_time


class PotentialFile(object):
	def __init__(self, file_path, potential_category):
		self.file_path = file_path
		self.potential_category = potential_category
