# Repetitive_Elements_Pipeline
This pipeline is implemented in the Python programming language. The purpose of the pipeline is to insert repetitive elements into genomes, break them apart into short reads, and then reassemble them to test the ability of the assemblers to deal with repetitive elements. 

There are 3 programs that this pipeline is dependent on which must be installed prior to running it:
* ART, a short read simulator
* SPAdes, an assembler
* Unicycler, another assembler

The pipeline currently uses 4 specific genomes, but these can be changed to any other genomes by modifying the `accession` variable. 
