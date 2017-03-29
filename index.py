
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

#db Entity

class SignUp(db.Model):
  firstname=db.StringProperty(required=True)
  lastname=db.StringProperty(required=True)
  username=db.StringProperty(required=True)
  password=db.StringProperty(required=True)
  #birthdate=db.DateProperty(required=True)
  email=db.EmailProperty(required=True)

class Handler(webapp2.RequestHandler):
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)

  def render_str(self,template,**param):
    t= jinja_env.get_template(template)
    return t.render(param)

  def render(self,template,**kw):
    self.write(self.render_str(template,**kw))

class SignUpPage(Handler):
  #this is wriiten in order to retain user name password upon invalid login 
  def render_SignUp_Page(self,title="",firstname="",lastname="",username="",password="",confirmpassword="",email="",birthdate="",error=""):
      self.render("signuppage.html",title=title,username=username,password=password,error=error)

  def get(self):
    self.render("signuppage.html")

  def post(self):
      firstname=self.request.get("firstname")
      lastname=self.request.get("lastname")
      email=self.request.get("email")
      birthdate=self.request.get("birthdate") 
      username=self.request.get("username")
      password=self.request.get("password")
      confirmpassword=self.request.get("confirmpassword")

      if(firstname and lastname and email and birthdate and username and password and confirmpassword):
      
        #db instance creation
        signup=SignUp(firstname=firstname,lastname=lastname,email=email,username=username,password=password)
        signup.put()
        signup=db.GqlQuery("select * from SignUp")
        firstname=[]
        for sign in signup:
          firstname.append(sign.firstname)
        self.render_SignUp_Page("signup",firstname,lastname,username,"","",email,birthdate,firstname)

        #self.redirect("/HomePage")
      else:
        self.render_SignUp_Page("signup",firstname,lastname,username,"","",email,birthdate,"some fields not not filled") 


class LoginPage(Handler):
  #this is wriiten in order to retain user name password upon invalid login 
   def render_Login_Page(self,title="",username="",password="",error=""):
      self.render("index.html",title=title,username=username,password=password,error=error)


      #cookies

      visits=self.request.cookies.get('visits',0)
      #if visits.isdigit():
      visits=int(visits)+1
      #else:
       # visits=0
      self.response.headers.add_header('set-cookie','visits=%s' % visits)
      self.write("you have here %s times" % visits)


   def get(self):
    self.render_Login_Page()

   def post(self):
    username=self.request.get("username")
    password=self.request.get("password")
    if username=='admin':
      self.redirect("/HomePage")
    else:
      self.render_Login_Page("login",username,password,"Invalid Login")

   
class HomePage(Handler):

   def get(self):
    #get from db
    username="swetha"
    signup=db.GqlQuery("select * from SignUp")
    print signup
    self.render("homepage.html",name=username,signup=signup)

class SetUpCookies(Handler):
  def get(self):
    visits=self.request.cookies.get('visits',0)
    if visits.isdigit():
      visits=int(visits)+1
    else:
      visits=0


    self.response.header.add_header('set-cookie','visits=%s',visits)
    self.write("you have here %s times" % visits)

app = webapp2.WSGIApplication([('/', LoginPage),('/HomePage',HomePage),('/SignUp',SignUpPage),('/SetUpCookies',SetUpCookies)], debug=True)
