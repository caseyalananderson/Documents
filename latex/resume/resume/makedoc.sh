#!/bin/bash

xe=xelatex
bi=biber

tex=resume_main.tex
bcf=resume_main.bcf
pdf=resume_main.pdf

# comiple resume
$xe $tex
$bi $bcf
$xe $tex

#open $pdf
gnome-open $pdf
