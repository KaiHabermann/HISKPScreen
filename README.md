To view Webpage:
- ensure docker, docker-compse are installed:
  - sudo apt-get update  
  - sudo apt-get install -y docker
  - sudo apt-get install -y docker-compose
  - (maybe needed) sudo service start docker
- sudo docker-compose up 
- type localhost:8000 into your webbrowser
- enjoy

To add new page to rotation:
- create hmtl file in static folder
- add hmtl to pages variable in views.py
