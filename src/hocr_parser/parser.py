__author__ = 'Rafa Haro <rh@athento.com>'

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import re


class HOCRElement:

    __metaclass__ = ABCMeta

    COORDINATES_PATTERN = re.compile("bbox\s(-?[0-9]+)\s(-?[0-9]+)\s(-?[0-9]+)\s(-?[0-9]+)")

    def __init__(self, hocr_html, next_tag, next_attribute, next_class):
        self.__coordinates = (0, 0, 0, 0)
        self._hocr_html = hocr_html
        self._elements = self._parse(next_tag, next_attribute, next_class)

    def _parse(self, next_tag, next_attributte, next_class):
        try:
            title = self._hocr_html['title']
            match = HOCRElement.COORDINATES_PATTERN.search(title)
            if match:
                self.__coordinates = (match.group(1), match.group(2), match.group(3), match.group(4))
            else:
                raise ValueError("The HOCR element doesn't contain a valid title property")
        except KeyError:
            self.__coordinates = (0, 0, 0, 0)

        elements = []
        if next_tag is not None and next_class is not None:
            for html_element in self._hocr_html.find_all(next_tag, {'class':next_attributte}):
                elements.append(next_class(html_element))
        return elements

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def html(self):
        return self._hocr_html.prettify()

    @property
    @abstractmethod
    def ocr_text(self):
        pass

class HOCRDocument(HOCRElement):

    def __init__(self, source, is_path=False):

        if not is_path:
            hocr_html = BeautifulSoup(source, 'html.parser')
        else:
            hocr_html = BeautifulSoup(open(source, 'r').read(), 'html.parser')

        super(HOCRDocument, self).__init__(hocr_html, 'div', Page.HOCR_PAGE_TAG, Page)

    @property
    def ocr_text(self):
        output = ""
        for element in self._elements[:-1]:
            output += element.ocr_text
            output += "\n\n"
        output += self._elements[-1].ocr_text
        return output

    @property
    def pages(self):
        return self._elements

    @property
    def npages(self):
        return len(self._elements)


class Page(HOCRElement):

    HOCR_PAGE_TAG = "ocr_page"

    def __init__(self, hocr_html):
        super(Page, self).__init__(hocr_html, 'div', Area.HOCR_AREA_TAG, Area)

    @property
    def ocr_text(self):
        output = ""
        for element in self._elements[:-1]:
            output += element.ocr_text
            output += "\n\n"
        output += self._elements[-1].ocr_text
        return output

    @property
    def areas(self):
        return self._elements

    @property
    def nareas(self):
        return len(self._elements)



class Area(HOCRElement):

    HOCR_AREA_TAG = "ocr_carea"

    def __init__(self, hocr_html):
        super(Area, self).__init__(hocr_html, 'span', Line.HOCR_LINE_TAG, Line)

    @property
    def lines(self):
        return self._elements

    @property
    def nlines(self):
        return len(self._elements)

    @property
    def ocr_text(self):
        output = ""
        for element in self._elements[:-1]:
            output += element.ocr_text
            output += "\n"
        output += self._elements[-1].ocr_text
        return output


class Line(HOCRElement):

    HOCR_LINE_TAG = "ocr_line"

    def __init__(self, hocr_html):
        super(Line, self).__init__(hocr_html, 'span', Word.HOCR_WORD_TAG, Word)

    @property
    def words(self):
        return self._elements

    @property
    def nwords(self):
        return len(self._elements)

    @property
    def ocr_text(self):
        output = ""
        for element in self._elements[:-1]:
            output += element.ocr_text
            output += " "
        output += self._elements[-1].ocr_text
        return output


class Word(HOCRElement):

    HOCR_WORD_TAG = "ocrx_word"

    def __init__(self, hocr_html):
        super(Word, self).__init__(hocr_html, None, None, None)

    @property
    def ocr_text(self):
        word = self._hocr_html.string
        if word is not None:
            return word
        else:
            return ""