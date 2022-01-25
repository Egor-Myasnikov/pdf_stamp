from collections import OrderedDict

import PyPDF2 as pypdf
import xmltodict
import pdfkit


def merge_pdf(orig_path, second_path, out_path):
    with open(orig_path, "rb") as inFile, open(second_path, "rb") as overlay:
        original = pypdf.PdfFileReader(inFile)
        background = original.getPage(0)
        foreground = pypdf.PdfFileReader(overlay).getPage(0)

        # merge the first two pages
        background.mergePage(foreground)

        # add all pages to a writer
        writer = pypdf.PdfFileWriter()
        for i in range(original.getNumPages()):
            page = original.getPage(i)
            writer.addPage(page)

        # write everything in the writer to a file
        with open(out_path, "wb") as outFile:
            writer.write(outFile)


def prepare_xml(delom_path):
    delom_xml = open(delom_path, 'r')
    xml = xmltodict.parse(delom_xml.read())

    pages = {}

    # registrationStamps
    for stamps in xml['document']:
        if isinstance(xml['document'][stamps], OrderedDict):
            for stamp_name in xml['document'][stamps]:
                if isinstance(xml['document'][stamps][stamp_name], OrderedDict):
                    stamp = xml['document'][stamps][stamp_name]
                    page_num = stamp['position']['page']
                    if page_num not in pages:
                        pages[page_num] = []

                    pages[page_num].append({
                        'name': stamp['@filename'],
                        'pos': (int(stamp['position']['topLeft']['x']), int(stamp['position']['topLeft']['y'])),
                        'dimension': (int(stamp['position']['dimension']['w']), int(stamp['position']['dimension']['h']))
                    })

    return pages


def save_stamp_pdf(tmp_str, path):
    WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'

    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    pdfkit.from_string(tmp_str, str(path), configuration=config, options={
        '--enable-local-file-access': ''
    })

