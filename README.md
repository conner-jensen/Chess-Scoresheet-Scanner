# Chess-Scoresheet-Scanner

Chess Scoresheet Scanner is a Python application to convert a handwritten chess scoresheet into a PGN file + Lichess link.

![Project thumbnail|width=100](/assets/thumbnail.png)

## Getting Started
### Dependencies
This project requires Python and the following libraries:
* OpenCV
* Numpy
* TensorFlow
* python-chess
### Installation
1. Clone the repository:
  ```bash
  git clone https://github.com/conner-jensen/Chess-Scoresheet-Scanner/
  cd yourproject
  ```
2. Install the dependencies:
  ```
  pip install -r requirements.txt
  ```

## Usage

1. During your game, use the [custom printable scoresheet](printable_scoresheet.pdf) to record your moves
    - Write neatly with **no overlapping letters** and **no touching the move boxes**
2. Take a photo of your completed scoresheet and up
3. Run [main.py](/Scoresheet/main.py) with `image_path` pointing to your photo
4. Follow the terminal instructions to correct any errors
