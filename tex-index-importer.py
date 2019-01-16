#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Alexandre D'Hondt"
__version__ = "1.0"
__copyright__ = "AGPLv3 (http://www.gnu.org/licenses/agpl.html)"
__doc__ = """
This tool aims to import course index pages (scanned, processed with Tesseract
 OCR, or as raw text) and to convert them into valid index entries in TeX
 format. It also allows to import entries directly into an IDX file.
"""
__examples__ = [
    "-s page-1.jpg page-2.jpg",
    "-fs page-1.txt page-*.jpg",
    "page-*.txt -o main.idx",
    "page-*.txt -ro main.idx",
]

# --------------------- IMPORTS SECTION ---------------------
import glob
import string
import unidecode
from PIL import Image
from tinyscript import *
try:
    import pyocr
except ImportError:
    print("Missing dependencies, please run 'sudo pip install pyocr'")
    sys.exit(1)


# --------------------- CONFIG SECTION ----------------------
AMBIG_LEVEL = 25
logging.addLevelName(AMBIG_LEVEL, "AMBIGUITY")
def ambiguity(self, m, *a, **kw):
    if self.isEnabledFor(AMBIG_LEVEL):
        self._log(AMBIG_LEVEL, "\033[33m{}\033[0m".format(m), a, **kw)
logging.Logger.ambiguity = ambiguity


# --------------------- CLASSES SECTION ---------------------
class AlreadyProcessed(Exception):
    """ Custom exception class for handling already OCR-processed files. """
    pass


class ExtendAction(argparse.Action):
    """ Custom input list extension argparse action. """
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        items = [i for sl in items for i in sl]  # flatten collected values
        setattr(namespace, self.dest, items)


class Index(dict):
    """
    Index dictionary structured as follows:
        { [entry:str]: { [book_number:str]: [refs:list(str)] } }

    :param filename: input file to be parsed for inclusion in the dictionary
    """
    sep = ":"
    common_ocr_mistakes = {
        '.d11': ".dll",
        'mds': "md5",
        'MDs': "MD5",
    }
    entry_val = re.compile(r'^(?P<b>\d+){0}(?P<p>\d+(?:\-+\d+)?)$'.format(sep))
    entry_err = [re.compile(r'^(\d+)$'), re.compile(r'^(\d+)(?:\-+(\d+))?$')]

    def __init__(self, filename=None):
        super(Index, self).__init__()
        self.__max_book_len = 1
        self.__tokens = []
        if filename is not None:
            for page in Index.pages(filename):
                self.update(page)

    def count(self):
        """
        Counts the current number of references in the index dictionary.

        :return: number of references
        """
        s = 0
        for entry, refs in self.items():
            for l in refs.values():
                s += len(l)
        return s

    def merge(self, dst, rewrite=False):
        """
        Opens a given destionation IDX file, retrieves imported index entries to
         add them into the index dictionary and then writes the new entries to
         the same file, thus merging the old and new entries.

        :param dst:     output file descriptor
        :param rewrite: rewrite the import section, dropping previous results
        """
        if dst is None:
            return
        title = "IMPORTED ENTRIES (DO NOT MOVE THIS SECTION ELSEWHERE !)"
        header = "\comment{" + 93 * '*' + '\n' + 18 * ' '  + title + '\n' + \
                 101 * '*' + '}'
        entries = []
        # first load the IDX file
        fn = os.path.basename(dst.name)
        content = dst.read()
        dst.close()
        # if it has an imported entries section, append these to self
        old_refs = 0
        if header in content:
            content, imported = content.split(header, 1)
            if not rewrite:
                s = self.sep
                for l in imported.split('\n'):
                    if len(l) == 0:
                        continue
                    if l.startswith("\comment{"):
                        l = l[9:-1].strip()
                    if l.startswith("\indexentry{"):
                        parts, p = l[12:-1].split("}{")
                        if "|book{" in parts:
                            parts, b = parts.split("|book{", 1)
                            b = b[:-1]
                        if '!' in parts:
                            parts, _ = parts.split('!', 1)
                        e = parts
                        self.setdefault(e, {})
                        self[e].setdefault(b, [])
                        if p not in self[e][b]:
                            self[e][b].append(p)
                            logger.debug("{} > {}{}{}".format(e, b, s, p))
                        else:
                            old_refs += 1
        else:
            content += '\n' * 3
        n = self.count() - old_refs
        if n > 0:
            # now write the new imported entries section to the IDX file
            with open(fn, 'w') as f:
                f.write(content + header + '\n' + self.to_idx())
            logger.debug("Added {} new references".format(n))
        else:
            logger.debug("No change")

    def to_idx(self):
        """
        Converts the index dictionary to a TeX index file.

        :return: list of \indexentry{...}
        """
        idx = {}
        for entry, refs in self.items():
            for i, _ in enumerate(sorted(refs.items(), key=lambda x: x[0])):
                book, pages = _
                idx.setdefault(book, [])
                for r, page in enumerate(pages):
                    idx[book].append("\indexentry{%s%s%s}{%s}" % (entry,
                        "" if i == 0 else "!" + i * " ",
                        "|book{" + book + "}" if r == 0 else "", page))
        return '\n\n'.join('\n'.join(e) for _, e in \
               sorted(idx.items(), key=lambda x: x[0]))

    def update(self, src=None, fix=False):
        """
        Updates the dictionary with the references found in the given content.

        :param src: raw text content to be included in the index dictionary
        :param fix: fix OCR ambiguities manually by prompting for user choice
        """
        if src is None:
            logger.error("No input text")
            return
        entry, is_last_token_ref = [], False
        # filter commented lines
        src = '\n'.join(filter(lambda x: re.search(r'^\s*\#\s*', x) is None,
                               src.split('\n')))
        # transform the source text to tokens
        tokens = map(lambda x: x.strip("., "),
                     re.split("\s+", ' '.join(src.split('\n'))))
        # function for creating a new reference on the current index entry
        def new_reference(token):
            if len(entry) > 0:
                e = ' '.join(entry).strip()
                # fix common OCR mistakes
                for old, new in self.common_ocr_mistakes.items():
                    e = e.replace(old, new)
                # fix LaTeX escaped characters
                for c in ['_', '&']:
                    e = e.replace(c, '\\' + c)
                # ensure the entry is created
                self.setdefault(e, {})
                if len(self[e]) == 0:
                    logger.debug("{}".format(e))
                # parse and add the reference
                logger.debug("> {}".format(token))
                m = self.entry_val.search(token)
                book, pages = m.group('b'), m.group('p')
                self.__max_book_len = max(self.__max_book_len, len(book))
                self[e].setdefault(book, [])
                self[e][book].append(pages)
            else:
                logger.warn("Passing reference '{}'...".format(token))
        # consume the tokens
        while len(tokens) > 0:
            token = tokens.pop(0)
            for c in ['-', '_']:
                token = re.sub(re.escape(c) + r'+', c, token)
            # pass single capital letter (category)
            if (len(token) == 1 and token in string.ascii_uppercase) or \
                token.lower() == "index":
                continue
            # add reference to the current index entry
            elif self.entry_val.match(token):
                new_reference(token)
                is_last_token_ref = True
            # a reference could have been recognized with error, handle by
            #  asking the user to resolve the token type
            elif fix and any(regex.match(token) for regex in self.entry_err):
                logger.ambiguity("Possibly erroneous token found: {}"
                                 .format(token))
                choice = None
                while choice not in ["1", "2"]:
                    choices = "(1) Index entry or (2) Reference ? [1|2]  "
                    try:  # Python2
                        choice = raw_input(choices).strip()
                    except NameError:  # Python3
                        choice = input(choices).strip()
                if choice == "1":
                    entry.append(token)
                else:
                    # fix the reference relying on the greatest length of book
                    #  number encountered up to now, then add the reference
                    i = self.__max_book_len
                    token = token[:i] + self.sep + token[i+1:]
                    new_reference(token)
                is_last_token_ref = choice != "1"
            # the token is handled as a new index entry part
            else:
                if is_last_token_ref:
                    entry = []
                entry.append(token)
                is_last_token_ref = False

    @staticmethod
    def pages(wildcard, ocr="libtesseract"):
        """
        Custom validation function for argparse input argument.

        :param files: input file wildcard or single file from command line args
        """
        assert ocr in ["libtesseract", "tesseract", "cuneiform"]
        logger.setLevel(logging.DEBUG)
        pages = []
        for fn in glob.iglob(wildcard):
            out = None
            # try first as an image
            try:
                img = Image.open(fn)
                ofn = fn + ".txt"
                if os.path.exists(ofn):
                    raise AlreadyProcessed()
                logger.info("Running PyOCR against '{}'...".format(fn))
                ocr = getattr(pyocr, ocr)
                bld = pyocr.builders.TextBuilder(tesseract_layout=6)
                out = ocr.image_to_string(img, lang="eng", builder=bld)
                out = unidecode.unidecode(out)
                with open(ofn, 'w') as f:
                    f.write(out)
            # if already OCR-processed, open the related text file
            except AlreadyProcessed:
                logger.debug("Image '{}' already processed by OCR".format(fn))
                fn = ofn
                with open(fn) as f:
                    out = f.read()
            # if not an image, open it as raw text
            except OSError:
                logger.debug("'{}' not an image".format(fn))
                with open(fn) as f:
                    out = f.read()
            except:
                logger.error("OCR failed for '{}'".format(fn))
            if out is not None:
                pages.append((os.path.basename(fn), out))
        return pages


# ---------------------- MAIN SECTION -----------------------
if __name__ == '__main__':
    parser.register('action', 'extend', ExtendAction)
    parser.add_argument("input", type=Index.pages, nargs='+', action="extend",
                        help="scanned index pages or text file\n"
                             " NB: supports file wildcards")
    parser.add_argument("-f", "--fix", action="store_true",
                        help="fix OCR ambiguities manually (default: false)")
    parser.add_argument("-o", "--output", type=argparse.FileType('r'),
                        help="output IDX file (default: none)")
    parser.add_argument("-r", "--rewrite", action="store_true",
                        help="rewrite the IDX result (default: false)\n"
                             " (that is, drop the previous imports)\n",
                        note="this option has no effect without -o")
    parser.add_argument("-s", "--show", action="store_true",
                        help="show the IDX result (default: false)")
    initialize(globals())
    index = Index()
    for fn, page in args.input:
        logger.info("Adding '{}'...".format(fn))
        index.update(page, args.fix)
    if args.show:
        logger.info("Resulting IDX:")
        print(index.to_idx())
    if args.output:
        fn = os.path.basename(args.output.name)
        logger.info("Merging IDX result with '{}'".format(fn))
        index.merge(args.output, args.rewrite)
