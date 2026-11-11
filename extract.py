import fitz

doc = fitz.open("sample.pdf")
for i, page in enumerate(doc, start=1):
    print("Page", i)
    print(page.get_text())