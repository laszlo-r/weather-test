
Hello
-----

A quick app to test weather data from openweathermap. Without registration, it just queries some samples from their api. A proper `APPID` could be set in `app.py` if desired.

Running `run.sh` generates a `weather-test` docker image and runs it on 0.0.0.0:8000. Change the port in the script as needed.

After that, should be able to curl against the service. Samples have limited data, one example: `curl http://localhost:8000/weather/london/20170216/1200`


Frontend stuff
--------------

The included `index.html` is a separate plain JS exercise for using a canvas plus generic responsiveness. 


Questions
---------
 - Kelvin?
   - Their api accepts specifying "?units=[K|metric|imperial]", so the view in this app could expect that and pass it along
 - Testing?
   - Would start with http://flask.pocoo.org/docs/1.0/testing/, use `test_request`, comparing results against expected results (stored as json fixtures)
 - Coverage?
   - Would start with http://flask.pocoo.org/docs/1.0/tutorial/tests/ and unittest, or maybe look at alternative test runners
 - Docs?
   - A good starting point: https://pypi.org/project/Flask-Autodoc/
 - Restricting access?
   - Implement auth along https://flask-login.readthedocs.io/en/latest/ and use `@login_required` on views
 - Daily updates?
   - Could schedule a daily bulk download (cron or celery if python preferred), more info: http://bulk.openweathermap.org/sample/
   - Store daily data in a database by timestamp, adding fresh ones in the daily job
