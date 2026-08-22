from parser import extract_text_from_pdf


pdf_path = "../data/Blood-Test-Descriptions.pdf"

text = extract_text_from_pdf(pdf_path)

print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")