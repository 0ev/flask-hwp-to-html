import subprocess
import uuid
import os
import bs4

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
        img['src'] = r"{{url_for('" + 'static' + r"', filename='tempfile/" + id + '/' +img['src'] + r"')}}"

    open(path+"/result.html", "w",encoding='UTF8').write(str(soup))
    

def change_to_html(path):

    id=str(uuid.uuid4())

    os.mkdir('/app/static/tempfile/'+id)

    subprocess.check_call(['/app/static/hwp5html.exe',"--output", "/app/static/tempfile/" + id , path])

    subprocess.check_call(['/app/static/hwp5html.exe',"--html","--output", "/app/static/tempfile/"+id+"/hey.html",path])

    combine("/app/static/tempfile/"+id)

    set_img("/app/static/tempfile/"+id,id)

    return id

