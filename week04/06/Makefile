.PHONY: clean

paper.pdf: paper.tex plot-data.png
	pdflatex paper.tex

plot-%.png: %.dat plot.py
	./plot.py -i $*.dat -o $@

clean: 
	rm -f paper.pdf
	rm -f $$(git ls-files --others --exclude-standard)
