# Repetitive_Elements_Pipeline
This pipeline is implemented in the Python programming language. The purpose of the pipeline is to insert repetitive elements into genomes, break them apart into short reads, and then reassemble them to test the ability of the assemblers to deal with repetitive elements. This pipeline was created by Hillary Dapsauski, Kimia Boreiri, and Joshua Melnick.


## Required Dependencies 
To utilize and run the pipeline, install the following dependencies and ensure that these dependencies are within the directory where you will be running the pipeline: 

- **Python** - [Download](https://www.python.org/downloads/)
- **ART** - [Download](https://www.niehs.nih.gov/research/resources/software/biostatistics/art) - use the MountRainier version 
- **SPAdes** - [GitHub](https://github.com/ablab/spades)
- **Unicycler** - [GitHub](https://github.com/rrwick/Unicycler)
- **QUAST** - [GitHub](https://github.com/ablab/quast)
- **Matplotlib** - [Download](https://matplotlib.org/stable/install/index.html)

The pipeline currently uses 4 specific genomes, but these can be changed to any other genomes by modifying the `accession` variable. 


## Running the pipeline 

To run the pipline use the following lines of code within the terminal. Make sure to run the pipeline within the directory called Repetitive_Elements_Pipeline or else this will not function properly. 

```bash
git clone https://github.com/h-dapsauski/Repetitive_Elements_Pipeline.git
cd Repetitive_Elements_Pipeline
python3 pipeline.py
```

## Pipeline steps
### Downloading the genomes
The pipeline begins by downloading the genomes from RefSeq if they have not already been downloaded. 
The 4 genomes we use by default are:
* Spiroplasma gladiatoris (https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_004379335.1/)
* Cruoricaptor ignavus (https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_014961145.1/)
* Pseudomonas sivasensis (https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_021391435.1/)
* Iamia majanohamensis (https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_028532485.1/)

However, the pipeline can be modified to use any genome. Simply update the `accession` variable in the `download_genomes` function with your desired accession codes.

### Insertion of repetitive elements
Next, repetitive elements are inserted into the pipeline to create artificial genomes. 

### Short read simulation
The artificial genomes are broken apart by ART as it simulates 150 bp paired end short reads from an Illumina sequencer. It does this at a depth of 10 and 100, but these values can be modified by changing the `depth` variable in the for loop of the `run_art` function. An example of a modified for loop that increments depth by 10 from 10 to 100 is available in the comments above the current for loop. 

The call to ART uses the following flags: 
* `-p` indicates paired ends
* `-na` omits the alignment files so ART just outputs the short reads
* `-i` is the input genome, which in this case is each modified genome
* `-l` is the read length, currently set to 151
* `-f` is the fold coverage, which means depth
* `-o` is the output prefix used for naming
* `-m` is the mean fragment length, set to 200
* `-s` is the standard deviation, set to 10

### Assembly
The short reads are then reassembled by SPAdes and Unicycler to compare their ability to handle repetitive elements.
