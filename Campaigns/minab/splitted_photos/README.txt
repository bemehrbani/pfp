SPLITTED CHILDREN PHOTOS
=========================

This folder contains 100 individual child photos extracted from the original image
`final-minab--01_scmx.jpg` using red borders as separators.

CONTENTS
--------
- 100 JPG files (child photos)
- name_correction.csv - For manual name correction
- mapping.txt - Mapping of child numbers to filenames and extracted names
- README.txt - This file

STATISTICS
----------
- Total children: 100
- Named with extracted text: 67 files
- Numbered fallback names: 33 files
- All photos are 350-450px wide, 600-750px tall

HOW TO USE
----------
1. Review photos: All child photos are named with the child's name where possible
2. For name corrections: Open `name_correction.csv` in a spreadsheet editor
   - Add correct names in the "suggested_correction" column
   - Names marked "YES" in "needs_correction" require attention
3. Rename files: After corrections, rename files accordingly

FILENAME FORMAT
---------------
- Named files: FirstName_LastName_XX.jpg (XX = border index)
- Numbered files: child_XXX.jpg (XXX = child index 001-100)

NOTES
-----
- Some names may be incorrect due to OCR limitations
- Arabic/Persian script names are preserved in filenames where extracted
- Manual verification recommended for critical accuracy

For detailed process documentation, see ../FINAL_SUMMARY.md