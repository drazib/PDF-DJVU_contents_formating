# PDF-DJVU_contents_formating
Small Python module to format the table of contents for inclusion in a  PDF or DJVU file.


## Initial contents file formating
The input file 'contents.txt' must be formated this way:
- number of spaces at the beginning of the line indicates the level;
- the number at the end of the line indicates the page;
- (blank lines are ignored).

Output defaults to 'contents.bmk'.

One liner, provided the contents is written in 'contents.txt':
> from contents import Contents

> Contents().writePDFcontents()

## Use of output contents file
### DJVU files
Use the two following commands:
> djvused -e print-outline book.djvu

> djvused -s -e 'set-outline contents.bmk' book.djvu

### PDF files
First, get the metadata of the PDF file:
> pdftk file.pdf dump_data > metadata.txt

Then, modify the metadata file by including contents.bmk after the line containing the keyword "NumberOfPages:".

Finally, updade the PDf metadata:
> pdftk file.pdf update_info metadata.txt output newfile.pdf
