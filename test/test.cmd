set base=%*

del %base%.json
del %base%.slides.json
del %base%.pptx

python ../md2json.py -i %base%.md -o %base%.json
python ../json2slide.py -i %base%.json -o %base%.slides.json
python ../json2pptx.py -i %base%.slides.json -o %base%.pptx -r ../refs/default.pptx

start %base%.pptx