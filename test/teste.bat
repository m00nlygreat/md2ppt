set filename=%*
python3 ../md2json.py -f %filename%.md -e
python3 ../json2slide.py -f %filename%.json -e %filename%_slides.json
python3 ../json2pptx.py -i %filename%_slides.json -o %filename%.pptx -r ref.ppt
start %filename%.pptx