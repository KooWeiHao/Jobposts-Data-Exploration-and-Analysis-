#GitHub link: https://github.com/KooWeiHao/Jobposts-Data-Exploration-and-Analysis-

import os
import glob
import kaggle
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class technical_test:
	
	def __init__(self, data_url, data_path):
		self.data_url = data_url
		self.data_path = data_path

	#download Kaggle dataset
	def download_dataset(self):
		u = urlparse(self.data_url)
		dataset = u.path.strip('/')
		kaggle.api.dataset_download_files(dataset, path = self.data_path, unzip = True)

	#extract data from "jobpost" column & store in new dataframe
	def extract_data(self):
		csvfiles = glob.glob(os.path.join(self.data_path, '*.csv'))

		for csvfile in csvfiles:
			df = pd.read_csv(csvfile, usecols = ['jobpost'])
			df_data = []

			for i in df.index:
				content = df['jobpost'][i]
				content_data = []

				#job title
				if 'TITLE' in content:
					title_start = content.find('TITLE') + 6
					title_end = content.find('\r\n', title_start)
					title = content[title_start:title_end].strip()
					content_data.append(title)
				else:
					title = None
					content_data.append(title)

				#position duration
				if 'DURATION' in content:
					duration_start = content.find('DURATION') + 9
					duration_end = content.find('\r\n', duration_start)
					duration = content[duration_start:duration_end].strip()
					content_data.append(duration)
				else:
					duration = None
					content_data.append(duration)
				
				#position location
				if 'LOCATION' in content:
					location_start = content.find('LOCATION') + 9
					location_end = content.find('\r\n', location_start)
					location = content[location_start:location_end].strip()
					content_data.append(location)
				else:
					location = None
					content_data.append(location)

				#job description
				if 'DESCRIPTION' in content:
					desc_start = content.find('DESCRIPTION') + 12
					if 'JOB RESPONSIBILITIES' in content:
						desc_end = content.find('JOB RESPONSIBILITIES')
					elif 'RESPONSIBILITIES' in content:
						desc_end = content.find('RESPONSIBILITIES')
					elif 'REQUIRED QUALIFICATIONS' in content:
						desc_end = content.find('REQUIRED QUALIFICATIONS')
					else:
						desc_end = content.find('APPLICATION PROCEDURES')
					description = content[desc_start:desc_end].strip()
					content_data.append(description)
				else:
					description = None
					content_data.append(description)

				#job responsibilities
				if 'RESPONSIBILITIES' in content:
					resp_start = content.find('RESPONSIBILITIES') + 17
					resp_end = content.find('REQUIRED QUALIFICATIONS')
					responsibilities = content[resp_start:resp_end].strip()
					content_data.append(self.clean_text(responsibilities))
				else:
					responsibilities = None
					content_data.append(responsibilities)

				#required qualifications
				if 'QUALIFICATIONS' in content:
					qual_start = content.find('QUALIFICATIONS') + 15
					if 'REMUNERATION' in content:
						qual_end = content.find('REMUNERATION')
					else:
						qual_end = content.find('APPLICATION PROCEDURES')
					qualifications = content[qual_start:qual_end].strip()
					content_data.append(qualifications)
				else:
					qualifications = None
					content_data.append(qualifications)

				#remuneration
				if 'REMUNERATION' in content:
					ren_start = content.find('REMUNERATION') + 13
					ren_end = content.find('\r\n', ren_start)
					remuneration = content[ren_start:ren_end].strip()
					content_data.append(remuneration)
				else:
					remuneration = None
					content_data.append(remuneration)

				#application deadline
				if 'DEADLINE' in content:
					deadline_start = content.find('DEADLINE') + 9
					deadline_end = content.find('\r\n', deadline_start)
					deadline = content[deadline_start:deadline_end].strip()
					content_data.append(deadline)
				else:
					deadline = None
					content_data.append(deadline)

				#about company
				if 'ABOUT COMPANY' in content:
					about_start = content.find('ABOUT COMPANY') + 14
					about_end = content.find('--')
					about_company = content[about_start:about_end].strip()
					content_data.append(about_company)
				else:
					about_company = None
					content_data.append(about_company)

				df_data.append(content_data)

			new_df = pd.DataFrame(df_data, columns = ['Job Title', 'Position Duration', 'Position Location', 'Job Description', 'Job Responsibilities', 'Required Qualifications', 'Remuneration', 'Application Deadline', 'About Company'])
			print(new_df)

	#identify the company with the most number of job ads in the past 2 years
	#identify the month with the largest number of job ads over the years
	#problem encountered: Some of the "year" from the "date" column are not able to be extracted and failed to figure out a way to standardize the date format in python code due to unknown problems
	#workaround: manually change the date format in the csv file
	def identify_company_month(self):
		csvfiles = glob.glob(os.path.join(self.data_path, '*.csv'))

		for csvfile in csvfiles:
			df = pd.read_csv(csvfile, usecols = ['jobpost', 'date'])
			df['date'] = pd.to_datetime(df['date'])
			df['year'], df['month'] = df['date'].dt.year, df['date'].dt.month_name() 
			current_year = datetime.now().year
			company_list = []

			for i in df.index:
				jobpost = df['jobpost'][i]
				year = df['year'][i]

				if (year >= current_year - 2) and (year < current_year):

					company_start = 0
					company_end = jobpost.find('\r\n')
					company = jobpost[company_start:company_end].strip()
					company_list.append(company)

			print("The company with the most number of job ads in the past 2 years is", max(set(company_list), key = company_list.count))
			print("-------------------------------------------------------------------------------")
			print("The month with the largest number of job ads over the years is", df['month'].value_counts().idxmax())

	#remove stop words & convert plural words into singular words
	def clean_text(self, text):
		stop_words = set(stopwords.words('english'))
		text = word_tokenize(text)
		new_text = []

		for word in text:
			if word not in stop_words:
				word = WordNetLemmatizer().lemmatize(word)
				new_text.append(word)

		return " ".join(new_text)

if __name__ == '__main__':
	data_url = "https://www.kaggle.com/madhab/jobposts"
	data_path = "C:/Users/User/Desktop/Dataset"

	test = technical_test(data_url, data_path)
	test.download_dataset()
	test.extract_data()
	test.identify_company_month()
