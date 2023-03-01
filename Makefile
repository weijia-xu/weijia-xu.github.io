SHELL=/bin/sh

all: publication.html

publication.html: scripts/publications.py scripts/generate_pubs.py
	set -e;\
	cd scripts;\
	python generate_pubs.py > ../publication.html;

docs/cv/cv.pdf: docs/cv/cv.tex
	set -e;\
	cd docs/cv;\
	pdflatex cv.tex;
