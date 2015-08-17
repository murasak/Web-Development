import webapp2
import cgi

def valid_month(month):
	months = ['January','February','March','April','May','June',
	'July','August','September','October','November','December']
	# Use diction to be user-friendly input, only input the abbrev for the month
	mon_abr = dict((m[:3].lower(), m) for m in months)
	if month:
		short_month = month[:3].lower()
		return mon_abr.get(short_month)

def valid_day(day):
	if day and day.isdigit():
		day = int(day)
		if day>0 and day<=31:
			return day

def valid_year(year):
	if year and year.isdigit():
		year = int(year)
		if year >1900 and year <2020:
			return year

# Escape '>','<','&','"' from the HTML
def escape_html(s):
	return cgi.escape(s, quote=True)

# method is GET by default.
form = """
<form method="post">
	What is your birthday?
	<br>
	<label> Month
		<input type="text" name="month" value="%(month)s">
	</label> 

	<label> Day
		<input type="text" name="day" value="%(day)s">
	</label> 

	<label> Year
		<input type="text" name="year" value="%(year)s">
	</label> 

	<div style="color:red">%(error)s</div>
	<br>
	<br>
	<input type = "submit">
</form>
"""

# ROT13 assignment
def reverse(s):
	list1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	list2 = "abcdefghijklmnopqrstuvwxyz"
	rot =""
	for elt in s:
		if elt in list1:
			index = list1.index(elt)
			if (index>=0 and index<13):
				rot += list1[index+13]
			elif (index>=13):
				rot += list1[index-13]
			
		elif elt in list2:
			index = list2.index(elt)
			if (index>=0 and index<13):
				rot += list2[index+13]
			elif (index>=13):
				rot += list2[index-13]
		else:
			rot += elt
	return (escape_html(rot))

myHtml = """
 <!DOCTYPE HTML>
 <html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome to my page.")

class FormHandler(webapp2.RequestHandler):
    def get(self):
        self.write_form()

    def post(self):
    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')

    	month = valid_month(user_month)
    	day = valid_day(user_day)
    	year = valid_year(user_year)

    	# Keep the user value in the text, instead of clearing the form
    	if not (month and day and year):
    		self.write_form("Invalid input.",user_month, user_day, user_year)
    	# Redirect to a successful URL, avoid requests for reposting and could share the URL
    	else:
    		self.redirect("/thanks") 
    		#/thanks is the path, no need to add http:// since it's in the same domain.

    def write_form(self, error="",month="",day="",year=""):
		self.response.out.write(form % {"error":error,
										"month":escape_html(month),
										"day":escape_html(day),
										"year":escape_html(year)})

# Redirect successful page
class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid day!")

# ROT13 app
class RotHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(myHtml % {"text":""})

	def post(self):
		user_text = self.request.get('text')
		self.response.out.write(myHtml % {"text":reverse(user_text)})


app = webapp2.WSGIApplication([
    ('/', MainHandler),('/unit2', FormHandler),('/thanks', ThanksHandler),
('/unit2/rot13', RotHandler),], debug=True)
