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
- Create new Branch and merge request

- Create hmtl file in static folder
- Put all your images in the image folder inside static
- We use django backend, so we can use some keys inside the html, as it is going to be rendered through django
- For the django documentation visit https://docs.djangoproject.com/en/4.2/
  - Important: The HTML should include the line ```{% load static %}``` 
  - After that line static data can be fetched like the following ``` url({% static '/images/HISKP_dark.png' %})``` where the root is the static folder
- The description of the merge request now needs the following:
  - A list of all html files, which should be added to rotation
  - A list of the outside dependencies (Websites, where data is grabbed from) per HTML.
  
- The TV has a 4K resolution. Thus if you want to be as secure as possible, just create a 4K PNG of whatever you want to show and you are set with a verry simple HTML
