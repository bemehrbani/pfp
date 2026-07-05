# Child Photo Splitting Process Summary

## Task
Split `final-minab--01_scmx.jpg` into individual child photos using red borders and name each photo with the child's name.

## Results
- **Successfully split**: 100 child photos extracted and filtered by size
- **Output folder**: `final_children/` containing `child_001.jpg` to `child_100.jpg`
- **Naming**: Numbered sequentially (OCR name extraction failed)
- **Documentation**: `README.md` and `name_mapping.txt` in output folder

## Technical Approach

### 1. Red Border Detection
Tried multiple approaches:
- **RGB thresholding**: Failed (image is CMYK)
- **CMYK color space**: Successful detection with thresholds: c<70, m>160, y>160, k<70
- **HSV color space**: Also successful with dual ranges: [0-10] and [170-180] hue
- **Final method**: OpenCV HSV detection with morphological closing

### 2. Image Splitting Methods
- **Grid line detection** (CMYK): Found 33 vertical, 19 horizontal lines → 680 cells (many non-child)
- **Contour detection** (OpenCV): Found 104 candidate borders, filtered to 100 valid child photos by size
- **Size filtering**: Kept only images 350-450px wide, 600-750px tall (typical child photo dimensions)

### 3. Name Extraction (OCR)
- **Attempted**: pytesseract with Farsi/Arabic/English language packs
- **Preprocessing**: Grayscale conversion, contrast enhancement, Otsu thresholding
- **Regions**: Bottom 20% of each photo (where names likely appear)
- **Result**: Failed to extract readable child names
- **Possible reasons**: Low resolution, handwritten text, stylized font, text outside cropped area

## Files Created

### Scripts
- `split_children.py`: Initial RGB-based attempt
- `debug_image.py`: Debug pixel colors (revealed CMYK mode)
- `find_red.py`: CMYK red detection
- `detect_borders.py`: Line detection in CMYK
- `split_red_borders.py`: HSV-based border detection
- `grid_detection.py`: Improved grid line detection
- `split_children_final.py`: Final contour-based splitting with OCR attempt
- `filter_children.py`: Size-based filtering
- `extract_names.py`: Farsi OCR name extraction
- `examine_child.py`: OCR debugging
- `copy_and_rename.py`: Final organization and renaming

### Intermediate Folders
- `splitted_photos/`: 863 cells from initial grid detection
- `splitted_photos_grid/`: 680 cells from improved grid detection
- `splitted_final/`: 104 photos from contour detection
- `children_final/`: 100 filtered child photos (350-450x600-750px)
- `children_named/`: Poorly OCR-named photos (not usable)
- `final_children/`: **Final output** - 100 numbered child photos

## Final Output
```
final_children/
├── README.md                    # Documentation
├── name_mapping.txt            # Original to final name mapping
├── child_001.jpg               # Child photo 1
├── child_002.jpg               # Child photo 2
...
└── child_100.jpg               # Child photo 100
```

## Usage
The 100 child photos are ready for use. If child names are available from another source, they can be manually renamed using the mapping file.

## Lessons Learned
1. **Color space matters**: CMYK images require different processing than RGB
2. **OCR limitations**: Text extraction from low-resolution images is unreliable
3. **Multiple approaches**: Grid detection vs contour detection have different strengths
4. **Post-processing**: Size filtering is essential to remove non-child cells

## Next Steps (if needed)
1. Manual naming if child name list is available
2. Try advanced OCR with custom Farsi training data
3. Extract text from original composite before splitting
4. Consider manual verification of OCR results