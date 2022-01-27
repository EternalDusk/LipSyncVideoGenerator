<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Lip Synced Character Animator Generator</h3>

  <p align="center">
    Automate the creation of lip synced characters easily utilizing only a transcript and an audio file!
    <br />
    <a href="https://github.com/github_username/repo_name/issues">Report Bugs and Issues</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>


<!-- GETTING STARTED -->
## Getting Started

This will show you how to get started with this project locally.

### Prerequisites

* FFmpeg
  ```
  Download from https://www.ffmpeg.org/
  ```
* Python 3.7.9 or above

* Required Python libraries
  ```
  colorama >=0.4.4
  Pillow >= 8.4.0
  ```

### Included requirements

* Praat (6.1.24) with SendPraat.exe (required for running commands)
* Montreal Forced Aligner with english detection libraries

### Installation

1. Clone the repo
   ```sh
   git clone https://https://github.com/EternalDusk/AutoVideoGenerator.git
   ```
2. Install required libraries
   ```
   pip install -r requirements.txt
   ```
3. Add your character files to the "character" folder (explained <a href="#character">here</a>)

4. Place your edited transcript and audio file into the "data" folder (transcript tags explained <a href="#usage">here</a>)



<!-- USAGE EXAMPLES -->
<div id="usage"></div>

## Usage

Use transcript tags to add different emotions and poses to your characters.

Simply enclose the pose name relating to the image in angled brackets, then add an underscore to the beginning.

### You must have an image matching the given tag

Example:

```
<_idle> I am recording some test audio

<_proud> to work with my

<_wave> automatic video editor.
```
To run the program with your selected data files:
```
main.py <audio file> <transcript file>
```

Audio files must be in '.wav' or '.mp3' format

Transcript files must be in '.txt' format

<!-- CHARACTER -->
 <div id="character"></div>

 ## Character

 Here is a list of the images required for this project.

 1) 1 image for each pose used in the tagged transcript

 2) 13 images used for mouth syncing inside "mouths" folder as follows:

      1.png - 'sil', 'sp', 'M', 'N', 'NG', 'P'

      2.png - 'AA', 'AO'

      3.png - 'R', 'AW', 'UW', 'W', 'AY', 'ER', 'AE', 'EY', 'S', 'UH', 'OY', 'OW', 'EH'

      4.png - 'AH'

      7.png - 'B'

      8.png - 'CH', 'SH', 'ZH'

      11.png - 'DH'

      12.png - 'F', 'V'

      13.png - 'H', 'HH'

      14.png - 'JH'

      15.png - 'K', 'G', 'D', 'IH', 'IY', 'S'

      18.png - 'T', 'Y', 'Z'

      19.png - 'TH', 'L'

(Yes I am aware the numbering is off)

<!-- ROADMAP -->
## Roadmap

- [ ] Add functionality to check for correct command syntax
- [ ] Add functionality to check for all necessary character files
    - [ ] Check for all referenced images needed from transcript
- [ ] Update phoneme numbering in program




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Tyler Wiseman - [@duskwiseman](https://twitter.com/duskwiseman) - wiseman.tyler.co@gmail.com

Project Link: [https://github.com/EternalDusk/AutoVideoGenerator](https://github.com/EternalDusk/AutoVideoGenerator)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Thanks to CaryKH for creating the 2 programs that inspired this project](https://www.youtube.com/watch?v=y3B8YqeLCpY)
