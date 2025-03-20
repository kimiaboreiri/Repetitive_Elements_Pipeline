import os

if not os.path.isdir("Genomes"):
    os.system("mkdir Genomes")

origseqs = ["GCF_014961145.1_ASM1496114v1_genomic.fna","GCF_028532485.1_ASM2853248v1_genomic.fna","GCF_021391435.1_ASM2139143v1_genomic.fna","GCF_004379335.1_ASM437933v1_genomic.fna"]

#add code to download sequences


#add code to insert repetitive elements


#add code to run art

#art flags: -i = input, -l = read length, -f = fold coverage, -o = output prefix, -m = mean fragment length, -s = standard deviation
os.system("art_illumina -i {0} -l 151 -f {1} -o {2}".format(genome,coverage,out))

#add code to run spades
os.system("spades.py -k 77 --careful -1 {0}_1.fastq -2 {0}_2.fastq -o {1}".format(name, outdir))

#add code to run unicycler