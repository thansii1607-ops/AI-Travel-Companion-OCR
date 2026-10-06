import pytesseract


def extract_text(image):

    text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    return text
