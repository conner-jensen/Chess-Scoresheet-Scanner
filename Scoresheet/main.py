from preprocessing import preprocess_image
from move_extraction import extract_move_boxes
from ocr import OCRModel
from postprocessing import OCRCorrector

def main():

    # Preprocess the image
    image_path = 'Scoresheet/input_images/example1.png'
    processed_image = preprocess_image(image_path)

    # Extract move boxes from the preprocessed images (as ROIs)
    move_boxes = extract_move_boxes(processed_image)

    # Initialize single-character OCR model
    ocr_model = OCRModel('Scoresheet/models/trained_model.h5')

    # Perform OCR on each move box; 'perform_ocr' returns top N predictions in a tuple of n candidates
    move_candidates = [ocr_model.perform_ocr(box, n=10) for box in move_boxes]

    # Remove blank move boxes
    move_candidates = [candidate for candidate in move_candidates if candidate != tuple()]

    # Error correct based on chess rules
    corrector = OCRCorrector()
    corrector.process_moves(move_candidates)
    print(corrector.get_lichess_url())
    # Done!


if __name__ == "__main__":
    main()