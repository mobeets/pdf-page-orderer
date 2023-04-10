import sys
import argparse

def get_front(npages, blank_page_name, xxx_todo_changeme, xxx_todo_changeme1):
    (outside_left,inside_left) = xxx_todo_changeme
    (inside_right,outside_right) = xxx_todo_changeme1
    left = inside_left
    right = inside_right
    if left > npages:
        left = blank_page_name
    if right > npages:
        right = blank_page_name
    return (left, right)

def get_back(npages, blank_page_name, xxx_todo_changeme2, xxx_todo_changeme3):
    (outside_left,inside_left) = xxx_todo_changeme2
    (inside_right,outside_right) = xxx_todo_changeme3
    left = outside_left
    right = outside_right
    if left > npages:
        left = blank_page_name
    if right > npages:
        right = blank_page_name
    return (left, right)

def get_page_order(npages, segments_per_sheet, offset, blank_page_name):
    """
    npages = number of pages of thing to be printed
        e.g. n = 27 pages
    segments_per_sheet = number of sets of 2-pages that will fit on one side of the printed sheet
        e.g. m = 2 would be A6 on A4
    """
    assert type(npages) is int
    assert type(segments_per_sheet) is int

    npages_with_blanks = 4*(int(npages / 4) + (npages % 4 > 0)) # round npages up to a multiple of 4
    assert npages_with_blanks % 4 == 0
    n_segments = int(npages_with_blanks/4)

    front_and_back_page_pairs = [(i, i+1) for i in range(offset+1, offset+npages_with_blanks+1, 2)]
    page_pairs_left_of_staple, page_pairs_right_of_staple = front_and_back_page_pairs[:n_segments], front_and_back_page_pairs[n_segments:]
    page_pairs_left_of_staple.reverse()

    segments = dict((i,{}) for i in range(n_segments))
    for i, (left_pages, right_pages) in enumerate(zip(page_pairs_left_of_staple, page_pairs_right_of_staple)):
        segments[i]['front'] = get_front(npages+offset, blank_page_name, left_pages, right_pages)
        segments[i]['back'] = get_back(npages+offset, blank_page_name, left_pages, right_pages)

    page_order = []
    get_segment = lambda ind, key: segments[ind][key] if ind in segments else (blank_page_name, blank_page_name)
    segments_per_group = int(n_segments/segments_per_sheet + (n_segments % segments_per_sheet > 0))
    for sheet_no in range(segments_per_group):
        # front page
        for j in range(segments_per_sheet):
            ind = j*segments_per_group + sheet_no
            page_order.extend(get_segment(ind, 'front'))
        # back page
        for j in range(segments_per_sheet):
            ind = j*segments_per_group + sheet_no
            page_order.extend(reversed(get_segment(ind, 'back')))

    # remove all indices higher than n, since these will be blank
    return page_order

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
