from string import ascii_lowercase
import itertools
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import random
import time
import sys

URL = 'https://www.game.co.uk/webapp/wcs/stores/servlet/HubArticleView?hubId=2837253&articleId=2837253&catalogId=10201&langId=44&storeId=10151&utm_source=Twitter&utm_medium=Organic'

USER_AGENT_LIST = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)

# Guide for form submission: https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python
def get_all_forms(session, url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    try:
      res.html.render()
    except:
      print('Error occurred. Timeout rendering... Sleeping for 10s')
      time.sleep(10)
      return None;
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def process_tag(tag_name, email):
  if (tag_name == 'EMAIL_ADDRESS_'):
    return email
  elif (tag_name == 'CONFIRM_DATA'):
    return 'Y'
  else:
    print('Unsupported tag name: ' + tag_name)
    return None

# Parse command line arguments
if len(sys.argv) != 2:
  print('Please run the command with a single argument: the target gmail email address')
  exit(1)
provided_email = sys.argv[1]
if not '@gmail.com' in provided_email:
  print('This script is designed to run with gmail addresses. Please create a gmail address and provide it instead.')
  exit(1)
starting_email = provided_email.replace('@gmail.com', '+{}@gmail.com')

for s in iter_all_strings():
  email = starting_email.format(s)
  print('Submitting for email: ' + email, flush=True)

  # initialize an HTTP session
  user_agent = random.choice(USER_AGENT_LIST)
  session = HTMLSession()
  session.headers.update({
    'User-Agent' : user_agent
  })
  forms = get_all_forms(session, URL)
  if not forms:
    continue;
  target_form = None
  for i, form in enumerate(forms, start=0):
    form_details = get_form_details(form)
    if form_details.get('action', "") == 'https://mailer1.game.co.uk/pub/rf':
      target_form = form_details
    
  if not target_form:
    print('Could not find target form', flush=True)
    exit(0)
  
  # the data body we want to submit
  data = {}
  for input_tag in target_form["inputs"]:
    if input_tag["type"] == "hidden":
      # if it's hidden, use the default value
      data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit":
      # all others except submit, prompt the user to set it
      data[input_tag["name"]] = process_tag(input_tag['name'], email)

  # join the url with the action (form request URL)
  url = urljoin(URL, target_form["action"])

  try:
    if form_details["method"] == "post":
      res = session.post(url, data=data)
    elif form_details["method"] == "get":
      res = session.get(url, params=data)
  except:
    print('Could not submit form', flush=True)
    continue

  # the below code is only for replacing relative URLs to absolute ones
  soup = BeautifulSoup(res.content, "html.parser")
  for link in soup.find_all("link"):
    try:
      link.attrs["href"] = urljoin(url, link.attrs["href"])
    except:
      pass
  for script in soup.find_all("script"):
    try:
      script.attrs["src"] = urljoin(url, script.attrs["src"])
    except:
      pass
  for img in soup.find_all("img"):
    try:
      img.attrs["src"] = urljoin(url, img.attrs["src"])
    except:
      pass
  for a in soup.find_all("a"):
    try:
      a.attrs["href"] = urljoin(url, a.attrs["href"])
    except:
      pass

  if res.status_code != 200:
    print('Failed! Non-200 status code', flush=True)
    exit(1)

  if not 'Your entry has been submitted' in str(soup):
    print('Failed! Form submission did not enter email into the giveaway.', flush=True)
    exit(1)
    
  # sleep to rate limit
  time.sleep(1)