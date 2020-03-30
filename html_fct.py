def html(title, links_lst=[], body=None):
    # links_lst = liste de dico
    links_str = ""
    for link in links_lst:
        attr_str = attr(link)
        links_str += "<link {} >".format(attr_str)
    return "<!DOCTYPE html><html><head><title>{}</title><meta charset=\"UTF-8\">{}</head>{}</html>".format(title, links_str, body)

def attr(attr_dic):
    str_attr = ""
    for at, val in attr_dic.items():
        str_attr += " {}=\"{}\" ".format(at, val)
    return str_attr

def body(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<body{}>{}</body>".format(attr_str, elem)

def header(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<header {}>{}</header>".format(attr_str, elem)

def footer(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<footer {}>{}</footer>".format(attr_str, elem)

def article(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<article {}>{}</article>".format(attr_str, elem)

def nav(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<nav {}>{}</nav>".format(attr_str, elem)

def aside(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<aside {}>{}</aside>".format(attr_str, elem)

def h1(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h1 {}>{}</h1>".format(attr_str, elem)

def h2(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h2 {}>{}</h2>".format(attr_str, elem)

def h3(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h3 {}>{}</h3>".format(attr_str, elem)

def h4(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h4{}>{}</h4>".format(attr_str, elem)

def h5(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h5 {}>{}</h5>".format(attr_str, elem)

def h6(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<h6 {}>{}</h6>".format(attr_str, elem)

def p(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<p {}>{}</p>".format(attr_str, elem)

def span(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<span {}>{}</span>".format(attr_str, elem)

def a(elem, attr_dic={}):
    attr_str = attr(attr_dic)
    return "<a {}>{}</a>".format(attr_dic, elem)




