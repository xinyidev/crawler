import fitz

def main():
    doc = fitz.open("【高级项目经理_深圳】唐黎 8年.pdf") # open a document
    for page in doc: # iterate the document pages
        text = page.get_text() # get plain text encoded as UTF-8
        print(text)

if __name__ == '__main__':
    main()