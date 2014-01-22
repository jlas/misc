#!/usr/bin/python
"""
Convert bank pdf statements to csv format.

Requires pdfminer (http://www.unixuser.org/~euske/python/pdfminer/)
"""

import os
import re
import sys

from cStringIO import StringIO
from pdfminer.converter import LTChar, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

DATERE = '[0-1]?[0-9]/[0-3]?[0-9]'
AMTRE = '[1-9](?:[,]?[0-9]{1,3})*\.[0-9]{2}'

# This class, originally from http://stackoverflow.com/a/1257121, has been
# modified to extract words that are on the same line by comparing the
# closeness of neighboring letters.
class CsvConverter(TextConverter):
    def __init__(self, *args, **kwargs):
        TextConverter.__init__(self, *args, **kwargs)

    def end_page(self, i):
        from collections import defaultdict
        lines = defaultdict(lambda : {})
        for child in self.cur_item._objs:
            if isinstance(child, LTChar):
                (_,_,x,y) = child.bbox
                line = lines[int(-y)]
                line[x] = child._text.encode(self.codec)

        for y in sorted(lines.keys()):
            # here we form words by finding characters that are close together
            line = lines[y]
            words = ['']
            lastx = 0.0
            for k, v in sorted(line.iteritems()):
                if not lastx:
                    lastx = k
                if abs(k - lastx) < 9.0:
                    words[-1] += v
                else:
                    words.append(v)
                lastx = k
            self.outfp.write(" ".join(words))
            self.outfp.write("\n")

# This function (slightly modified) from http://stackoverflow.com/a/1257121
def pdf_to_csv(filename):
    # ... the following part of the code is a remix of the
    # convert() function in the pdfminer/tools/pdf2text module
    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = CsvConverter(rsrc, outfp, codec="utf-8", laparams=LAParams())
    # becuase my test documents are utf-8 (note: utf-8 is the default codec)

    doc = PDFDocument()
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')

    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(doc.get_pages()):
        outfp.write("START PAGE %d\n" % i)
        if page is not None:
            interpreter.process_page(page)
        outfp.write("END PAGE %d\n" % i)

    device.close()
    fp.close()

    return outfp.getvalue()

def process_file(filename):
    """Process a statement pdf file to extract data about transactions,
    including date, amount, and description.
    """

    data = list()
    years = dict()
    deposit = False
    pdflines = pdf_to_csv(filename).split('\n')
    for line in pdflines:
        line = line.strip()

        # check if we are scanning throughh deposits or withdrawals
        linealt = line.replace(' ', '').lower()
        if 'depositsandothercredits' in linealt:
            deposit = True
        elif 'withdrawalsandservicefees' in linealt:
            deposit = False

        # find date range for year info
        found = re.findall('([0-1]?[0-9])/[0-3]?[0-9]/([12][0-9]{3})', line)
        if found:
            for mo, yr in found:
                years[mo] = yr

        match = re.match('(%s)[ ]*(%s)(.*)' % (DATERE, AMTRE) , line)
        if match:
            curdata = {'amt': '', 'date': '', 'desc': '', 'desc2': ''}

            # format date properly
            date = match.groups()[0]
            mo, dt = date.split('/')
            yr = years.get(mo, '2001')
            date = '%s-%s-%s' % (yr, mo, dt)
            curdata['date'] = date

            # format amount properly
            amt = match.groups()[1]
            if not deposit:
                amt = '-'+amt
            amt.replace(',', '')
            curdata['amt'] = amt

            # encountered a description
            curdata['desc'] = match.groups()[2].strip()
            data.append(curdata)

        elif data and not data[-1]['desc2']:
            # encountered second description line
            data[-1]['desc2'] = line
    return data

if __name__ == '__main__':

    # check for args
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print 'usage: %s <filename or directory>' % sys.argv[0]
        print """
%s is a python script that attempts to extract records from statements
saved as pdf documents.

It uses pdfminer to extract the text from these files.

Then it prints out the transactions in a csv format.
""" % sys.argv[0]
        sys.exit(1)

    files = []
    if os.path.isdir(sys.argv[1]):
        base = sys.argv[1]
        for f in os.listdir(base):
            files.append(os.path.join(base, f))
    else:
        files.append(sys.argv[1])

    data = list()
    for f in files:
        data += process_file(f)

    for d in sorted(data, key=lambda d: d['date']):
        print '%(date)s,%(desc)s %(desc2)s,%(amt)s' % d
