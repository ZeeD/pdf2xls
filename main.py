'main'

import glob
import sys
import typing

import pdf2xls.model.db
import pdf2xls.mtime.mtimereader
import pdf2xls.pdf2xls
import pdf2xls.reader.historyreader
import pdf2xls.reader.pdfreader
import pdf2xls.writer.xlswriter

HISTORY_DAT = 'history.dat'
OUTPUT_XLS = 'output.xlsx'


def main() -> None:
    'entry point'

    args: typing.List[str] = sys.argv[1:]

    db = pdf2xls.model.db.Db()

    try:
        f = open(HISTORY_DAT, 'rb')
    except FileNotFoundError:
        pass
    else:
        with f as history_file:
            mtime_reader = pdf2xls.mtime.mtimereader.MtimeReader(history_file)
            history_reader = pdf2xls.reader.historyreader.HistoryReader(history_file, mtime_reader)
            pdf2xls.pdf2xls.read_infos(history_reader, db)

    for arg in args:
        for file_name in glob.glob(arg):
            with open(file_name, 'rb') as pdf_file:
                mtime_reader = pdf2xls.mtime.mtimereader.MtimeReader(pdf_file)
                pdf_reader = pdf2xls.reader.pdfreader.PdfReader(pdf_file,
                                                                mtime_reader)
                pdf2xls.pdf2xls.read_infos(pdf_reader, db)

    with open(OUTPUT_XLS, 'wb') as xls_file:
        xls_writer = pdf2xls.writer.xlswriter.XlsWriter(xls_file)
        try:
            pdf2xls.pdf2xls.write_infos(xls_writer, db)
        finally:
            xls_writer.close()


if __name__ == '__main__':
    main()
