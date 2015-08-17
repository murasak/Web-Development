import webapp2
import cgi
import re

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
# SIGN-UP Assignment
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_pw(password):
	return PW_RE.match(password)

def valid_email(email):
	return EMAIL_RE.match(email)

signup = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(name_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(pw_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

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

# SIGN-UP APP
class SignHandler(webapp2.RequestHandler):
	def get(self):
		self.create_form()

	def post(self):
		user_name = self.request.get('username')
		user_pw = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')

		name = valid_username(user_name)
		pw = valid_pw(user_pw)
		email = valid_email(user_email)
		
		if not name:
			self.create_form("That's not a valid username.","","","",user_name,user_email)
		elif not pw:
			self.create_form("","That wasn't a valid password.","","",user_name,user_email)
		elif user_pw != user_verify:
			self.create_form("","","Your password didn't match.","",user_name,user_email)
		elif user_email != "" and not email:
			self.create_form("","","","That's not a valid email.",user_name,user_email)
		else:
			self.redirect("/welcome?username=" + user_name)

	def create_form(self, name_error="",pw_error="",verify_error="",email_error="",username="",email=""):
		self.response.out.write(signup % {"name_error":name_error,"pw_error":pw_error,
			"verify_error":verify_error,"email_error":email_error,
			"username":escape_html(username), "email":escape_html(email)})

class welcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("<h2>Welcome, %s !</h2>" % self.request.get('username'))

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/unit2', FormHandler),('/thanks', ThanksHandler),
('/unit2/rot13', RotHandler),('/unit2/signup',SignHandler),('/welcome',welcomeHandler),
], debug=True)
