import os

if not os.path.isdir("Genomes"): #make a directory to store genomes if it doesn't already exist
    os.system("mkdir Genomes")

origseqs = ["GCF_014961145.1_ASM1496114v1_genomic.fna","GCF_028532485.1_ASM2853248v1_genomic.fna","GCF_021391435.1_ASM2139143v1_genomic.fna","GCF_004379335.1_ASM437933v1_genomic.fna"]

#add code to download sequences


#add code to insert repetitive elements
#add code to insert repetitive elements
import os
#make file for modified genomes
os.makedirs("ModifiedGenomes")

#for the intial testing,we are only using motif lengths of 100pb and 500bp
#to confirm everything works before expanding to all lengths(100, 200, 300,400, 500)
motif_lengths = [100, 500]
repeat_count = [2, 3, 4, 5]

##original genomes list
genomes = [
    "GCF_014961145.1_ASM1496114v1_genomic.fna",
    "GCF_028532485.1_ASM2853248v1_genomic.fna",
    "GCF_021391435.1_ASM2139143v1_genomic.fna",
    "GCF_004379335.1_ASM437933v1_genomic.fna"
]

#Read the sequence
#loop over each genome file in the genomes list
for genomefile in genomes:
    with open(f"{genomefile}", "r") as f:
        lines = f.readlines()  #read lines and save in a list
        header = lines[0]   
        seq = ''.jon(lines[1:]).replace("\n", "") #combing alll remaining lines into one string/


## Loop over motif lenghts we want initially [100, 500]
        

for length in motif_lengths:
    motif = "ATGC" * (length // 4 )         #for making a motif with 100 bp length we need to multiple 4 bases 25 times
    






simgenomes = []

#add code to run art
if not os.path.isdir("artgens"): #directory for simulated genomes
    os.system("mkdir artgens") #create directory if it doesn't exist
os.chdir("artgens") #move to that directory

for genome in simgenomes:
    for coverage in range(10,110,10): #increase coverage from 10 to 100 in increments of 10
        #art flags: -i = input, -l = read length, -f = fold coverage, -o = output prefix, -m = mean fragment length, -s = standard deviation
        os.system("art_illumina -i {0} -l 151 -f {1} -o {2}".format(genome,coverage,out))

#add code to run spades
os.chdir("..") #exit the artgens directory
for name in os.listdir("artgens"): #assemble every simulated genome in the artgens directory
    os.system("spades.py -k 77 --careful -1 {0}_1.fastq -2 {0}_2.fastq -o {0}_assembly/".format(name))

import os
import subprocess
##directory to input files
input_dir = "/home/project3/artgens"

#making output file
output = "/home/project3/spades_output"
os.makedirs(output, exist_ok=True)

#raed1 files in input directory 
fq_files_read1 = []
for f in os.listdir(input_dir):
    if f.endswith('1.fq'):
        fq_files_read1.append(f)

#run SPAdes for each file
for fq1 in fq_files_read1:
    fq2 = fq1.replace('1.fq', '2.fq')

    fq1_path = os.path.join(input_dir, fq1)
    fq2_path = os.path.join(input_dir, fq2)
    
    #name for output
    base = fq1.replace('1.fq', '')
    outdir = os.path.join(output, base)
    os.makedirs(outdir, exist_ok=True)
    

    #run SPAdes
    subprocess.run(["spades.py", "-1", fq1_path, "-2", fq2_path, "-o", outdir])
    print(f"finish:{fq1} and {fq2} output in {outdir}")




import os
import subprocess

input_dir = "/home/project3/artgens"
output_dir = "/home/project3/unicycler_output"
os.makedirs(output_dir, exist_ok=True)

#forward read path

fq1_files =[]
for f in os.listdir(input_dir):
    if f.endswith('1.fq'):
        fq1_files.append(f)

for fq1 in fq1_files:
    fq2 = fq1.replace('1.fq', '2.fq')

    
    fq1_files_path = os.path.join(input_dir, fq1)
    fq2_files_path = os.path.join(input_dir, fq2)

    base1 = fq1.replace('1.fq', '')
    outdir1 = os.path.join(output_dir, base1)
    os.makedirs(outdir1, exist_ok=True)

##running unicycler
    subprocess.run(["unicycler", "-1", fq1_files_path, "-2", fq2_files_path, "-o", outdir1])
    print(f"unicycler finished")
