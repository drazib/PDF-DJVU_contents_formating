# -*- coding: utf-8 -*-
"""
Small Python module to format the table of contents for inclusion in a 
PDF or DJVU file.

# Initial contents file formating

The input file 'contents.txt' must be formated this way:

- number of spaces at the beginning of the line indicates the level;
- the number at the end of the line indicates the page;
- (blank lines are ignored);

Output defaults to 'contents.bmk'.


# Use of output contents file

## DJVU files

Use the two following commands:

> djvused -e print-outline book.djvu
> djvused -s -e 'set-outline contents.bmk' book.djvu


## PDF files

First, get the metadata of the PDF file:
> pdftk file.pdf dump_data > metadata.txt

Then, modify the metadata file by including contents.bmk after the line containing
the keyword "NumberOfPages:".

Finally, updade the PDf metadata:
> pdftk file.pdf update_info metadata.txt output newfile.pdf



Created on Thu Aug 20 13:20:10 2020

@author: dbrizard
"""

import os
import subprocess as sbp
import glob

import warnings



class Contents(object):
    """
    
    """
    def __init__(self, fname='contents.txt', pagesep=' ', indent=' ', debug=False):
        """
        
        :param str fname: file name
        :param str pagesep: page number separator
        :param str indent: indentation (level) separator
        :param bool debug: print lines for debugging purpose
        """
        
        with open(fname, 'r') as f:
            text = f.readlines()
        
        self.text = text # [xx.strip() for xx in text]
        self.pagesep = pagesep
        self.indent = indent
        
        self.treatLines(debug=debug)
    
    
    def treatLines(self, debug=False):
        """
        
        :param bool debug: print lines for debugging purpose
        """
        level = []
        title = []
        page = []
        for ll in self.text:
            #---Remove trailing \n---
            lll = ll.rstrip()
            if debug:
                print lll
                
            if not len(lll)==0:
                #---Count number of leading sep---
                ni = len(lll) - len(lll.lstrip(self.indent))
                level.append(ni+1)
                
                #---Get page number---
                ind = lll.rfind(self.pagesep)
                pagenumb = lll[ind+len(self.pagesep):]
                page.append(int(pagenumb))
                
                #---Get title---
                ttl = lll[:ind]
                title.append(ttl.strip())
        
        self.level = level
        self.page = page
        self.title = title
    
    
    def writePDFcontents(self, fname='contents.bmk', offset=0):
        """
        
        :param str fname: output filename
        :param int offset: page number offset
        """
        
        with open(fname, 'w') as f:
            for tt, ll, pp in zip(self.title, self.level, self.page):
                pp = pp + offset
                f.write('BookmarkBegin\n')
                f.write('BookmarkTitle: %s\n'%tt)
                f.write('BookmarkLevel: %i\n'%ll)
                f.write('BookmarkPageNumber: %i\n'%pp)
    
    
    def writeDJVUcontents(self, fname='contents.bmk', offset=0):
        """
        
        :param str fname: output filename
        :param int offset: page number offset
        """
        n = len(self.title)
        with open(fname, 'w') as f:
            f.write('(bookmarks\n')
            for ii, (tt, ll, pp) in enumerate(zip(self.title, self.level, self.page)):
                pp = pp + offset
                if ii<n-1:
                     if self.level[ii+1]==self.level[ii]:
                         # next is the same level
                         f.write('("%s" "#%i")\n'%(tt, pp))
                     elif self.level[ii+1]>self.level[ii]:
                         # there will be sublevels, keep parenthesis open
                         f.write('("%s" "#%i"\n'%(tt, pp))
                     elif self.level[ii+1]<self.level[ii]:
                         # no more sublevels, close parentheses
                         n_close = self.level[ii]-self.level[ii+1] +1
                         f.write('("%s" "#%i"'%(tt, pp)+' )'*n_close +'\n')
                else:
                    n_close = ll + 1
                    f.write('("%s" "#%i"'%(tt, pp)+' )'*n_close +'\n')


        
def addPDFtoc(pdffile=None):
    """
    
    """
    warnings.warn("This is not working yet..")
    #---GET PDF FILE---
    if pdffile is None:
        pdflist = glob.glob("*.pdf")
        if not len(pdflist)==0:
            if len(pdflist)>1:
                print "Several PDF files..."
                print pdflist
            pdffile = pdflist[0]
            print 
        else:
            print "/!\ no pdf files in the folder..."
            
    
    #---GET META DATA---
    sbp.call(['pdftk %s dump_data meta.txt'%pdffile])
    
    #---SUPPOSE CONTENTS.BMK IS HERE---
    Contents().writePDFcontents()
    with open("contents.bmk") as f:
        cont = f.read()
    
    #---MODIFY META.TXT---
    with open('meta.txt', 'r') as f:
        meta = f.readlines()
    
    # find line with "NumberOfPages"
    for ii, ll in enumerate(meta[:20]):
        if 'NumberOfPages' in ll:
            ind = ii
    
    # write new meta.txt file
    meta.insert(ind, cont)
    meta2 = "".join(meta)
    # https://stackoverflow.com/questions/10507230/insert-line-at-middle-of-file-with-python
    with open("meta2.txt", 'r') as f:
        f.write(meta2)
    
    #---ADD CONTENTS TO PDF FILE---
    sbp.call(['pdftk', pdffile, 'update_info meta2.txt output test.pdf'])
        
    
        
    

if __name__=='__main__':
    
    C = Contents('contents.txt', debug=True)
    C.writePDFcontents('test.bmk')
    C.writeDJVUcontents('testdjvu.bmk')
    
    #---TEST ADDPDFTOC---
    if False:
        print "TTTTTTTTTTTTTT"
        addPDFtoc()
    
