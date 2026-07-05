# Split Children Photos

## Source Image
- final-minab--01_scmx.jpg (original composite image)

## Processing Steps
1. Red border detection using OpenCV HSV color space
2. Contour detection to find individual photo borders
3. Size filtering (350-450px width, 600-750px height)
4. Result: 100 child photos

## Naming
Photos are numbered child_001.jpg to child_100.jpg since OCR text extraction
failed to recover child names from the images.

## Files
- child_001.jpg ... child_100.jpg: Individual child photos
- name_mapping.txt: Mapping from original filtered names to final names

## OCR Attempt
Attempted Farsi/Arabic/English OCR using pytesseract with various preprocessing
(contrast enhancement, thresholding, different page segmentation modes).
No readable child names were extracted, likely due to:
- Low text resolution
- Handwritten text
- Text outside cropped regions
- Insufficient contrast

## Scripts Used
- split_children_final.py: Main splitting with contour detection
- filter_children.py: Size-based filtering
- extract_names.py: OCR name extraction (unsuccessful)
