__author__ = 'Rafa Haro <rh@athento.com>'

def test_hocr():
    import os
    from hocr_parser.parser import HOCRDocument

    filename = "output.hocr"
    dir_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(dir_path, filename)
    document = HOCRDocument(full_path, is_path=True)
    assert document.npages == 1
    page = document.pages[0]
    assert page.parent == document
    assert page.coordinates == (0, 0, 545, 771)
    assert page.id == 'page_1'
    assert page.nareas == 3
    area = page.areas[0]
    assert area.parent == page
    assert area.coordinates == (83, 68, 449, 376)
    assert area.nparagraphs == 2
    assert area.paragraphs[0].lines[0].nwords == 1
    assert area.paragraphs[0].lines[0].ocr_text == area.paragraphs[0].lines[0].words[0].ocr_text == "|"
    assert area.paragraphs[1].nlines == 10

    area2_text = """At the remote terminal.
demodulation reconstructs the video
signal, which is used to modulate the
density ofprint produced by a
printing device. This device is
scanning in a raster scan
synchronised with that at the
transmitting terminal. As a result, a
facsimile copy of the subject
document is produced."""

    area1_line2 = "In facsimilea photocell is caused"
    assert area.paragraphs[1].lines[0].ocr_text == area1_line2

    area = page.areas[1]
    assert area.ocr_text == area2_text







