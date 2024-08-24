# sqlalchemy-challenge

The following repository is composed of 
SurfsUp 
	app.py --> python code to accomplish API SQLite Connection & Landing Page
	climate_starter.ipynb --> Jupiter lab code to accomplish Precipitation and Station Analysis
	Resources --> csv files and sqlite files to analyze. 
 ON app.py:
 	we use Dictionary Comprehension: The code {date: prcp for date, prcp in precipitation_data} creates a dictionary where:
		Each 'date' from the query results is a key.
		Each 'prcp' value (precipitation) is the corresponding value.
