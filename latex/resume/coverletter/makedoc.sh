#!/bin/bash

xe=xelatex
bi=biber

tex=coverletter_main.tex
bcf=coverletter_main.bcf
pdf=coverletter_main.pdf

# comiple resume
$xe $tex
$bi $bcf
$xe $tex

gnome-open $pdf
