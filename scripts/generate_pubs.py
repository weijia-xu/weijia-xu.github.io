import sys
from people import *
from publications import *
from venue import *

fout = sys.stdout

title_format = '<a href="{link}">{name}</a>'
author_format = '<a href="{link}"><span class="author">{name}</span></a>{symbol}'
venue_format = '<i>{abr}</i>, {year}<br>'

def gen_title(pub):
    if 'pdf' in pub:
        title = title_format.format(link=pub['pdf'], name=pub['title'])
    else:
        title = '%s' % pub['title']
    if 'award' in pub:
        name, link = pub['award']
        award = ' (<a href="{link}"><span class="award">{name}</span></a>)'.format(name=name, link=link)
    else:
        award = ''
    return '%s.%s<br>' % (title, award)

def gen_author(pub):
    s = []
    for author in pub['author']:
        symbol = ''
        if author in pub.get('equal', []):
            symbol = '*'
        name, link = people[author]
        s.append(author_format.format(link=link, name=name, symbol=symbol))
    return r'%s and %s.<br>' % (', '.join(s[:-1]), s[-1])

def gen_venue(pub):
    name, abr = venue[pub['venue']]
    if pub['type'] == 'arxiv':
        return '<i>{name}:{index} preprint</i>, {year}<br>'.format(name=name, index=pub['index'], year=pub['year'])
    elif pub['type'] == 'workshop':
        return '<i>{venue} Workshop on {name}</i>, {year}<br>'.format(venue=abr, name=name, year=pub['year'])
    elif pub['type'] == 'demo':
        return '<i>{name} ({abr}) demo, {year}</i>'.format(name=name, abr=abr, year=pub['year'])
    elif abr:
        return venue_format.format(abr=abr, year=pub['year'])
    else:
        return '<i>{name}</i>, {year}<br>'.format(name=name, year=pub['year'])

def gen_bib(pub):
    s = []
    for author in pub['author']:
        if author == 'hal':
            s.append("Hal {Daum\\'{e} III}")
        elif author == 'alvin':
            s.append('Alvin {Grissom II}')
        else:
            s.append(people[author][0])
    author = ' and '.join(s)

    type_ = pub['type']
    conf, abr = venue[pub['venue']]

    if type_ == 'conference':
        bib = """@inproceedings{{{name},
        author={{{author}}},
        title={{{title}}},
        booktitle={{{conference} ({abr})}},
        year={{{year}}}\n}}""".\
                    format(name=pub['bib'], \
                    author=author, \
                    title=pub['title'], \
                    conference=conf, abr=abr, year=pub['year'])
    elif type_ == 'arxiv':
        bib = """@article{{{name},
        author={{{author}}},
        title={{{title}}},
        journal={{arXiv:{index}}},
        year={{{year}}}\n}}""".\
                    format(name=pub['bib'], \
                    author=author, \
                    title=pub['title'], \
                    index=pub['index'], year=pub['year'])
    elif type_ == 'workshop':
        name, abr = venue[pub['venue']]
        bib = """@inproceedings{{{name},
        author={{{author}}},
        title={{{title}}},
        booktitle={{{venue} Workshop on {ws}}},
        year={{{year}}}\n}}""".\
                    format(name=pub['bib'], \
                    author=author, \
                    title=pub['title'], \
                    venue=abr, \
                    ws=name, year=pub['year'])

    return bib

def gen_resource(i, pub):
    s = []
    bib_div = None
    if 'bib' in pub:
        s.append('[<a href="javascript:copy(div{idx}, bib{idx})">bib</a>]'.format(idx=i))
        bib_div = '<div id="div{idx}"></div><div id="bib{idx}" style="display:none">\n<div class="bib">\n<pre>\n{bibtex}\n</pre>\n</div>\n</div>'.format(idx=i, bibtex=gen_bib(pub))

    for key in ['code', 'data', 'slides', 'poster', 'screencast', 'talk', 'project']:
        if key in pub:
            s.append('[<a href="{link}">{name}</a>]'.format(link=pub[key], name=key))

    return '%s<br>\n%s' % ('\n'.join(s), bib_div if bib_div else '')

curr_year = None
for i, pub in enumerate(pubs):
    if pub['year'] != curr_year:
        fout.write('<p><b>%s</b></p>\n' % pub['year'])
        curr_year = pub['year']
    fout.write('{title}\n{author}\n{venue}\n{resource}\n<br>\n'.format(title=gen_title(pub), author=gen_author(pub), venue=gen_venue(pub), resource=gen_resource(i, pub)))