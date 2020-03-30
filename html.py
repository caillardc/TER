def html(title, links_lst=[], body=None):
    # links_lst = liste de dico
    links_str = ""
    for link in links_lst:
        attr_str = ""
        for k,v in link.items():
            attr_str += " {}=\"{}\" ".format(k,v)
        links_str += "<link {} >".format(attr_str)
    return "<!DOCTYPE html><html><head><title>{}</title>{}</head>{}</html>".format(title, links_str, body)

def body(elem):
    return "<body>{}</body>".format(elem)

def header(elem):
    return "<header>{}</header>".format(elem)

def footer(elem):
    return "<footer>{}</footer>".format(elem)

def article(elem):
    return "<article>{}</article>".format(elem)

def nav(elem):
    return "<nav>{}</nav>".format(elem)

def aside(elem):
    return "<aside>{}</aside>".format(elem)

def h1(elem):
    return "<h1>{}</h1>".format(elem)

def h2(elem):
    return "<h2>{}</h2>".format(elem)

def h3(elem):
    return "<h3>{}</h3>".format(elem)

def h4(elem):
    return "<h4>{}</h4>".format(elem)

def h5(elem):
    return "<h5>{}</h5>".format(elem)

def h6(elem):
    return "<h6>{}</h6>".format(elem)

def p(elem):
    return "<p>{}</p>".format(elem)

def span(elem):
    return "<span>{}</span>".format(elem)

def a(elem, href, target="_self"):
    return "<a {} href=\"{}\" target=\"{}\">".format(elem, href, target)

titre = header(h1("Titre du document"))
texte = article(p("Texte explicatif"))
body = body(titre+texte)
page = html(title="Page 1", links_lst=[{"rel" : "stylesheet", "href" : "style1.css"}], body=body)

print(page)

