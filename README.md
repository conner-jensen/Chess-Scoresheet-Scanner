# Chess-Scoresheet-Scanner

Chess Scoresheet Scanner is a Python application to convert a handwritten chess scoresheet into a PGN file and Lichess link—without the use of any external OCR engine or vision model.

![Project thumbnail|width=100](/assets/thumbnail.png)

## Getting Started
### Dependencies
This project requires Python and the following libraries:
* OpenCV
* Numpy
* TensorFlow
* python-chess
### Installation
1. Clone the repository and enter the project:
  ```bash
  git clone https://github.com/conner-jensen/Chess-Scoresheet-Scanner/
  cd chess-scoresheet-scanner
  cd scoresheet
  ```
2. Install the dependencies:
  ```
  pip install -r requirements.txt
  ```
## Usage

#### 1. Use the Scoresheet
- Download and print the [custom scoresheet](Scoresheet/printable_scoresheet.pdf) to use in your next chess game.
- Write neatly in print, not cursive.
    - **No overlapping letters**
    - **No letters touching the move boxes**
#### 2. Take a Photo
- Take a clear photo of the scoresheet using your smartphone or camera.
    - Ensure all four corners are included in the image.
#### 3. Process the Scoresheet
- Place the photo in the project folder.
- Run the following program from the `/scoresheet` directory:
```bash
python main.py --image path/to/your/photo.jpg  
```
- Follow the terminal instructions to correct any errors
