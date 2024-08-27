# sqlalchemy-challenge

The following repository is composed of 
SurfsUp 
	app.py --> python code to accomplish API SQLite Connection & Landing Page
	climate_starter.ipynb --> Jupiter lab code to accomplish Precipitation and Station Analysis
	Resources --> csv files and sqlite files to analyze. 

 On the app.py Error Handling blocks were added for ease and clarity. I have the following comments:
     - The finally block is used when you want to ensure that certain actions (like closing a session) happen regardless of whether an exception is raised or not. Even if an error occurs within the try block, the finally block will execute, making it reliable for resource management.
     - session = Session(engine) is open and closed on each route.
     