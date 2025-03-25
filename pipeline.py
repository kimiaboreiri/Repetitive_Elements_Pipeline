import os

if not os.path.isdir("Genomes"): #make a directory to store genomes if it doesn't already exist
    os.system("mkdir Genomes")

origseqs = ["GCF_014961145.1_ASM1496114v1_genomic.fna","GCF_028532485.1_ASM2853248v1_genomic.fna","GCF_021391435.1_ASM2139143v1_genomic.fna","GCF_004379335.1_ASM437933v1_genomic.fna"] #list of what the genome files should download as
origseqcount = 0 #keeps track of which sequence file when checking downloads
accession = ["GCF_014961145.1","GCF_028532485.1","GCF_021391435.1","GCF_004379335.1"] #genome accession codes

for x in accession: #loop through accessions
    if origseqs[origseqcount] not in os.listdir("Genomes"): #the order of the files listed above is the same as the order of the accessions, so check if the file has already been downloaded before calling the accession code
        os.system(f"datasets download genome accession {x} --include genome") #download genome from refseq
        os.system("unzip ncbi_dataset.zip") #unzip
        os.system("rm ncbi_dataset.zip") #delete zip file which has generic name to prevent overwrite issues
        os.system("mv ncbi_dataset/data/GCF*/GCF* Genomes") #extract the genome file and move it to Genomes folder
        os.system("rm -rf ncbi_dataset/data") #delete the unzipped folder which has unnecessary extra stuff
        os.system("rm README.md") #delete extra file to avoid asking for overwrite
        os.system("rm md5sum.txt") #delete extra file to avoid asking for overwrite
        os.system("rmdir ncbi_dataset") #remove empty folder
    origseqcount += 1 #keep track of the file you are on

    

#add code to insert repetitive elements

#make directory for modified genomes
if not os.path.isdir("ModifiedGenomes"):
    os.makedirs("ModifiedGenomes")

#for the intial testing,we are only using motif lengths of 100pb and 500bp
#to confirm everything works before expanding to all lengths(100, 200, 300,400, 500)
motif_lengths = [100, 500]
repeat_count = [2, 3, 4, 5]

##original genomes list
genomes = []
for file in os.listdir("Genomes"):
    genomes.append(file)

'''genomes = [
    "GCF_014961145.1_ASM1496114v1_genomic.fna",
    "GCF_028532485.1_ASM2853248v1_genomic.fna",
    "GCF_021391435.1_ASM2139143v1_genomic.fna",
    "GCF_004379335.1_ASM437933v1_genomic.fna"
]'''

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

for gen in genomes:
    #for depth in range(10,110,10): #increase depth from 10 to 100 in increments of 10
    for depth in [10,100]: #runs art with depth of 10 and 100
        out = str(gen.split("_")[0]) + "_" + str(gen.split("_")[1]) + "_" + str(depth)
        #art flags: -i = input, -l = read length, -f = fold coverage, -o = output prefix, -m = mean fragment length, -s = standard deviation
        if not os.path.isfile("{}.fq".format(out)):
            os.system("art_illumina -i ../Genomes/{0} -l 151 -f {1} -o {2}".format(gen,depth,out))

#add code to run spades
os.chdir("..") #exit the artgens directory
for name in os.listdir("artgens"): #assemble every simulated genome in the artgens directory
    os.system("spades.py -k 77 --careful -1 {0}_1.fastq -2 {0}_2.fastq -o {0}_assembly/".format(name))

#add code to run unicycler
