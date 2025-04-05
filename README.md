# Repetitive_Elements_Pipeline
This pipeline is implemented in the Python programming language. The purpose of the pipeline is to insert repetitive elements into genomes, break them apart into short reads, and then reassemble them to test the ability of the assemblers to deal with repetitive elements. 


## Required Dependencies 
To untilize and run the pipeline, install the following dependencies and ensure that these dependencies are within the directory where you will be running the pipeline: 

- **Python** - [Download](https://www.python.org/downloads/)
- **ART** - [Download](https://www.niehs.nih.gov/research/resources/software/biostatistics/art) - use the MountRainier version 
- **SPAdes** - [GitHub](https://github.com/ablab/spades)
- **Unicycler** - [GitHub](https://github.com/rrwick/Unicycler)

The pipeline currently uses 4 specific genomes, but these can be changed to any other genomes by modifying the `accession` variable. 


## Running the pipeline 

To run the pipline use the following lines of code within the terminal. Make sure to run the pipeline within the directory called Repetitive_Elements_Pipeline or else this will not function properly. 

```bash
git clone https://github.com/h-dapsauski/Repetitive_Elements_Pipeline.git
cd Repetitive_Elements_Pipeline
python3 pipeline.py
```
