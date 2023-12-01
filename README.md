# Image-Face-Aligner
This is A CLI program i made before to try to recreate the iconic selfie every day timelapses over a couple of years but using my own script instead of manually editing it in another software

The projects uses a venv in order to use a specific version of python with mediapipe and contain all dependencies

# Usage
First create these in your working directory:
1. A folder containing all your unprocessed images
1. An empty folder for the script to use
1. A blank .gif file to export to

Then start the venv using:
```bash
Scripts\activate.bat
```
### Commands:
- `rename`:
    <br> renames images in the order they are going to be processed in
    - `-source_folder, -sf`-> name of images folder
    - `-new_name, -n, -prefix`-> prefix for renaming e.g "img-"
    - `-start_n, -sn, -from`-> starting number of images (useful if you only need to process new images and add them to previous)
- `align`: 
    <br> processes images to be ready for export
    - `-source_folder, -sf`-> name of images folder
    - `-destination_folder, -df`-> name of folder to put processed images in
- `export-gif`:
    <br> exports files in processed folder to a gif
    - `-source_folder, -sf`-> name of folder with processed images
    - `-destination_file, -exporting_file, -ef`-> name of blank .gif file to export to
    - [optional] `-duration, -d`-> time of one frame(in ms) in gif, default is 175
- `all`:
    <br> runs rename, align and export-gif with default values( not good for just adding some images)
    <br><br>default values:
    <br>source_folder->"images"
    <br>prefix->"IMG-"
    <br>destination_folder->"processed"
    <br>exporting_file->"exported.gif"
    <br>duration->175
    <br>you can use any of the previous tags to edit one/multiple default values
- `empty-folder`:
    <br> only for convenience of deleting all files in images/processed-images folder
    <br>`-folder, -f`-> name of folder to empty

use: ```python3 run.py [command] [options]```
for each of rename, align and export-gif in this order or just use all

you can close the venv using:
```bash
Scripts\deactivate.bat
```

# Credits and modules used
- image croppper: Philipp Wagner
- mediapipe
- cv2
- PIL
- click
- colorama