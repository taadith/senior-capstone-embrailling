# Load our dependencies
import pybrl as brl
# import chardet

filename = "Braille_Test.pdf"     # of course :P
pdf_password = None
language = 'english'

# Let's translate the PDF file.
translated = brl.translatePDF(filename, password = pdf_password, language = language) # Easy, right?

# Let's explore what this object looks like:

# print(len(translated))             # = 2 (One for each page)
# print(len(translated[0]))          # = 1 group of text in the page. 
#                                 #     There might be more if (i.e.) a box of text is in a corner.

# print(translated[0][0].keys())     # type, text, layout
# print(translated[0][0]['type'])    # 'text'
# print(translated[0][0]['layout'])  # The bounding box of this group

# print(translated[0][0]['text'][0]) # The first word: ['000001', '111000', '101010', '111010', '100010', '101100']

tex = ""                         # Template contents and what will be edited.
output = "output.tex"            # Output path to the tex file
TEMPLATE_PATH = "template.tex"   # Path to the Template tex file

with open(TEMPLATE_PATH, 'r', encoding='ISO-8859-1') as f:
    tex = f.read()

# Concatenate all the text. 
content = ""

for page in translated:
    for group in page:
        grouptxt = group['text']
        
        # Convert to Unicode characters:
        unicode_brl = brl.toUnicodeSymbols(grouptxt, flatten=True)
        content += "\n\n" + unicode_brl

# Create the new TeX
output_tex = tex.replace("%%% Content will go here %%%", content)

# Save it
with open(output, "w") as f:
    f.write(output_tex)


