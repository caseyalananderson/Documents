#!/bin/bash

tex='timeline.tex'
pdf='timeline.pdf'

pdflatex --jobname=timelinefig-f1 $tex
gnome-open timelinefig-f1.pdf
