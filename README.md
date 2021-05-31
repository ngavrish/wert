Python 3.7+

How to run:
-
python install -r requirements
pytest -s -q --alluredir allure-results
 
To view allure report you should have local allure web server 
configured on allure-results folder.

Why pytest:
-
Pytest was chosen, as personal preference. 
You can automate same logic using anything, including bash/powershell-script.

Additional thoughts: 
-
- Add commandline parametrisation
- Define test data more precisely - NASA is expected to have images when requested
- Add parallelism
- Current REST requests are mostly silent in console/logs. Should add something
like RESTAssured or another util level to give mote inside in test logs on 
whats been sent and what is returned 
 