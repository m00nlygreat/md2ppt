python3 ../md2json.py -f flattened.md -e
python3 ../json2slide.py -f flattened.json -e flattened_slides.json
python3 ../json2pptx.py -i flattened_slides.json -o output.pptx -r ref.pptx
start output.pptx