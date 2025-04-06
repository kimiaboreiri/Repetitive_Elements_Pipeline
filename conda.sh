#!/bin/bash

mkdir -p /home/project3/quast
cd /home/project3/quast

wget -nc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh -b -p /home/project3/quast/miniconda3

source /home/project3/quast/miniconda3/bin/activate

conda init bash
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

conda create -n compbio python=3.9 -y
conda activate compbio

conda install -c bioconda quast -y