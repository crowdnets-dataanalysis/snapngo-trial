import requests
url = 'https://files.slack.com/files-pri/T0512Q25E90-F05BYE1U746/download/archie.jpeg'
token = 'xoxb-5036818184306-5368561656855-PrENQrfNSbZOjskeOuWBBO1k'
r = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
filename = "archie.jpeg"
open(filename, 'wb').write(r.content)