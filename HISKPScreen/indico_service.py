from bs4 import BeautifulSoup
import requests


__week_plan_file__ = "static/week_plan.html"
_week_plan_image_path__ = "static/images/week_plan.png"




def get_indico_screengrab():
    link = "https://indico.hiskp.uni-bonn.de/category/0/overview?date=2022-04-04&period=month&detail=event"



def get_week_plan():
    return __week_plan_file__
    link = "https://indico.hiskp.uni-bonn.de/category/0/overview?date=2022-04-04&period=month&detail=event"
    
    url = requests.get(link)
    htmltext = url.text
    DOMdocument = BeautifulSoup(htmltext, 'html.parser')
    # print(DOMdocument)
    dates_block = DOMdocument.find_all(class_="content-column")
    # print(DOMdocument.find_all('head'))
    # dates_block = DOMdocument
    with open(__week_plan_file__,"w") as f:
        f.write(str(DOMdocument.find_all('head')[0])+ "".join([str(d) for d in dates_block]))
    return __week_plan_file__


if __name__ == "__main__":
    get_indico_screengrab()