import subprocess
import uuid
import os
import bs4

current_path=os.path.dirname(__file__)

print(current_path)

static_path=os.path.join(current_path,'static')

print(static_path)

temp_path=os.path.join(static_path,'tempfile')

def combine(path):
    soup = bs4.BeautifulSoup(open(path+"/hey.html",'r',encoding='UTF8').read(),features="lxml")
    stylesheets = soup.findAll("link", {"rel": "stylesheet"})
    for s in stylesheets:
        t = soup.new_tag('style')
        c = bs4.element.NavigableString(open(path+'/'+s["href"],'r',encoding='UTF8').read())
        t.insert(0,c)
        t['type'] = 'text/css'
        s.replaceWith(t)

    open(path+"/result.html", "w",encoding='UTF8').write(str(soup))

def set_img(path,id):
    soup = bs4.BeautifulSoup(open(path+"/result.html",'r',encoding='UTF8').read(),features="lxml")

    for img in soup.findAll('img'):
        try:
            img['src'] = r"{{url_for('" + 'static' + r"', filename='tempfile/" + id + '/' +img['src'] + r"')}}"
        except:
            pass
    open(path+"/result.html", "w",encoding='UTF8').write(str(soup))
    

def change_to_html(path):

    id=str(uuid.uuid4())

    os.mkdir(os.path.join(temp_path,id))

    subprocess.check_call([os.path.join(static_path,'hwp5html.exe'),"--output", os.path.join(temp_path, id) , path])

    subprocess.check_call([os.path.join(static_path,'hwp5html.exe'),"--html","--output", os.path.join(temp_path,id,"hey.html"),path])

    combine(os.path.join(temp_path,id))

    set_img(os.path.join(temp_path,id),id)

    print(id)

    return id
