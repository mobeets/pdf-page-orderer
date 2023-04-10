import sys
import argparse
from pyPdf import PdfFileWriter, PdfFileReader
from .page_orderer import get_page_order

def read(infile):
    return PdfFileReader(open(infile, "rb"))

def write(outfile, output):
    outputStream = open(outfile, "wb")
    output.write(outputStream)
    outputStream.close()

def title(inp):
    return inp.getDocumentInfo().title

def get_npages(inp):
    return inp.getNumPages()

def reorder(outfile, inp, page_order):
    dims = lambda: (inp.getPage(0).mediaBox.getWidth(), inp.getPage(0).mediaBox.getHeight())
    output = PdfFileWriter()
    for page_index in page_order:
        if page_index:
            output.addPage(inp.getPage(page_index-1))
        else:
            output.addBlankPage(*dims())
            # output.addPage(blank_page())
    write(outfile, output)

def reorder_main(infile, outfile, pairs_per_sheet, start_page):
    inp = read(infile)
    print('Read {0}.'.format(infile))
    npages = get_npages(inp)
    print('Found {0} pages.'.format(npages))
    page_order = get_page_order(npages, pairs_per_sheet, start_page, None)
    print('Reordering pages (None is BLANK): {0}'.format(', '.join([str(x) for x in page_order])))
    reorder(outfile, inp, page_order)
    print('Wrote to {0}.'.format(outfile))

def main():
    desc_msg = "Outputs the proper page ordering for printing a double-sided booklet"
    ex_msg = "example:\n"
    ex_msg += "    python page_orderer.py --pages 27 --pairs_per_sheet 2 --start_page 1 --blank_page BLANK\n"
    ex_msg += "\n"
    ex_msg += "    This would print 27 pages of A6 frames onto A4, since you can fit 2 pairs of A6 pages onto A4.\n"
    ex_msg += "    Simply arrange the pages in the order this script outputs; then cut, stack, and staple!\n"

    parser = argparse.ArgumentParser(
            prog='python pdf_booklet.py',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=desc_msg,
            epilog=ex_msg)
    parser.add_argument('--infile', type=str, required=True, help='the input .pdf file')
    parser.add_argument('--outfile', type=str, required=True, help='the output .pdf file')
    parser.add_argument('--pairs_per_sheet', type=int, required=True, help='number of pairs of input pages on single output page')
    parser.add_argument('--start_page', type=int, default=1, help='input start page')
    args = parser.parse_args(sys.argv[1:])
    def print_illegal(msg):
        parser.print_help()
        print()
        print(msg)
        exit(-1)
    if args.start_page <= 0 or args.pairs_per_sheet <= 0:
        print_illegal('--pages and --pairs_per_sheet must be positive')
    reorder_main(args.infile, args.outfile, args.pairs_per_sheet, args.start_page-1)

if __name__ == '__main__':
    main()
