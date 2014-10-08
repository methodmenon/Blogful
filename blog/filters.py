from blog import app

#date formatting filter created b/c Jinja does not include a date formatting filter by default

@app.template_filter()
def dateformat(date, format):
	#the date argument is piped in from the template
	#format string we provide as an argument
	if not date:
		return None
	return date.strftime(format)