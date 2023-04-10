import sys
import argparse
from bin import get_page_order

def main():
    desc_msg = "Outputs the proper page ordering for printing a double-sided booklet"
    ex_msg = "example:\n"
    ex_msg += "    python page_orderer.py --pages 27 --pairs_per_sheet 2 --start_page 1 --blank_page BLANK\n"
    ex_msg += "\n"
    ex_msg += "    This would print 27 pages of A6 frames onto A4, since you can fit 2 pairs of A6 pages onto A4.\n"
    ex_msg += "    Simply arrange the pages in the order this script outputs; then cut, stack, and staple!\n"

    parser = argparse.ArgumentParser(
            prog='python page_orderer.py',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=desc_msg,
            epilog=ex_msg)
    parser.add_argument('--pages', type=int, required=True, help='number of input pages')
    parser.add_argument('--pairs_per_sheet', type=int, required=True, help='number of pairs of input pages on single output page')
    parser.add_argument('--start_page', type=int, default=1, help='input start page')
    parser.add_argument('--blank_page', default='BLANK', help='label for blank page')
    args = parser.parse_args(sys.argv[1:])
    def print_illegal(msg):
        parser.print_help()
        print()
        print(msg)
        exit(-1)
    if args.start_page <= 0 or args.pages <= 0 or args.pairs_per_sheet <= 0:
        print_illegal('--pages and --pairs_per_sheet must be positive')
    res = get_page_order(args.pages, args.pairs_per_sheet, args.start_page-1, args.blank_page)
    print()
    print(','.join([str(x) for x in res]))
    print()

if __name__ == '__main__':
    main()
