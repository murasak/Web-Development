import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_pw(password):
	return PW_RE.match(password)

def valid_email(email):
	return EMAIL_RE.match(email)

def escape_html(s):
	return cgi.escape(s, quote=True)

myHtml = """
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
		self.write_form()

	def post(self):
		user_name = self.request.get('username')
		user_pw = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')

		name = valid_username(user_name)
		pw = valid_pw(user_pw)
		email = valid_email(user_email)
		
		if not name:
			self.write_form("That's not a valid username.","","","",user_name,user_email)
		elif not pw:
			self.write_form("","That wasn't a valid password.","","",user_name,user_email)
		elif user_pw != user_verify:
			self.write_form("","","Your password didn't match.","",user_name,user_email)
		elif user_email != "" and not email:
			self.write_form("","","","That's not a valid email.",user_name,user_email)
		else:
			self.redirect("/welcome?username=" + user_name)

	def write_form(self, name_error="",pw_error="",verify_error="",email_error="",username="",email=""):
		self.response.out.write(myHtml % {"name_error":name_error,"pw_error":pw_error,
			"verify_error":verify_error,"email_error":email_error,
			"username":escape_html(username), "email":escape_html(email)})

class welcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("<h2>Welcome, %s !</h2>" % self.request.get('username'))

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', welcomeHandler),
], debug=True)
