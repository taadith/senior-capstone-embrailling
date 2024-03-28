# Load our dependencies
import pybrl as brl
import subprocess
import boto3


s3 = boto3.resource('s3')

def translate_to_braille(filename, pdf_password=None, language='english'):
    # Print out bucket names
    my_bucket = s3.Bucket('filestorageembraillerbucket185717-staging')
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)

    translated = brl.translatePDF(filename, password = pdf_password, language = language) # Easy, right?

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
     
    subprocess.run(['xelatex', 'output.tex'], check=True)
    # print("PDF generated successfully.")

    with open('output.pdf', 'rb') as data:
        s3.Bucket('filestorageembraillerbucket185717-staging').put_object(Key='output.pdf', Body=data)


