#!/bin/bash

xe=xelatex
bi=biber

tex=references_main.tex
bcf=references_main.bcf
pdf=references_main.pdf

# comiple references
$xe $tex
$bi $bcf
$xe $tex

#open $pdf
gnome-open $pdf
