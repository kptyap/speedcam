from PyPDF2 import PdfFileWriter, PdfFileReader

output = PdfFileWriter()
input1 = PdfFileReader(open("speedcam 30jan.pdf", "rb"))


# print how many pages input1 has:
print "document1.pdf has %d pages." % input1.getNumPages()



# add page 1 from input1 to output document, unchanged
#output.addPage(input1.getPage(0))

# finally, write "output" to document-output.pdf
#outputStream = file("PyPDF2-output.pdf", "wb")
#output.write(outputStream)

##pageObj.extractText()

