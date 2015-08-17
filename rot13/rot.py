import webapp2
import cgi

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

list1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
list2 = "abcdefghijklmnopqrstuvwxyz"
def escape_html(s):
	return cgi.escape(s, quote=True)

def reverse(s):
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

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(myHtml % {"text":""})

	def post(self):
		user_text = self.request.get('text')
		self.response.out.write(myHtml % {"text":reverse(user_text)})

app = webapp2.WSGIApplication([
    ('/unit2/rot13', MainHandler)
], debug=True)
