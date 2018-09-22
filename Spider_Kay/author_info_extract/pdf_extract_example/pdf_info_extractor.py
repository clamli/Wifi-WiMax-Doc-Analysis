import fitz

from nltk import word_tokenize, pos_tag, ne_chunk
def getContent(path):
    doc = fitz.open(path)
    page = doc.loadPage(1)
    content = page.getText("text")
    print(content)
    findPersonName(content)

def findPersonName(content):
    result = ne_chunk(pos_tag(word_tokenize(content)))
    print(result)
if __name__ == "__main__":
    print(fitz.__doc__)
    path = "F:\\WireLessNLPGRA\\code\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\author_info_extract\\pdf_extract_example\\17__16-17-0018-01-Gdoc-p802-16s-to-sponsor-ballot-conditional-approval-request.pdf"
    getContent(path)
    