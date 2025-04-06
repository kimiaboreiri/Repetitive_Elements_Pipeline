import os 
import subprocess
import random 

# Joshua's Code - Downloading Genomes 
def download_genomes():
    if not os.path.isdir("Genomes"): #make a directory to store genomes if it doesn't already exist 
        os.system("mkdir Genomes")

    accession = ["GCF_014961145.1","GCF_028532485.1","GCF_021391435.1","GCF_004379335.1"] # genome accession codes 

    for x in accession: #loop through accessions
        if x not in ",".join(os.listdir("Genomes")): #no need to redownload 
            os.system(f"datasets download genome accession {x} --include genome") #download genome from refseq
            os.system("unzip ncbi_dataset.zip") #unzip
            os.system("rm ncbi_dataset.zip") #delete zip file which has generic name to prevent overwrite issues
            os.system("mv ncbi_dataset/data/GCF*/GCF* Genomes") #extract the genome file and move it to Genomes folder
            os.system("rm -rf ncbi_dataset/data") #delete the unzipped folder which has unnecessary extra stuff
            os.system("rm README.md") #delete extra file to avoid asking for overwrite
            os.system("rm md5sum.txt") #delete extra file to avoid asking for overwrite
            os.system("rmdir ncbi_dataset") #remove empty folder


# Hillary's Code - Generating and Inserting Repeats 
# This function is still a work in progress and needs more editting 
def generate_and_insert_repeats():
    bases = ["A", "C", "G", "T"] #nucleotide bases

    # 100 BP random repetitive element 
    motif1 = random.choices(bases, k=100) #100bp random sequence
    seq = "".join(motif1) #join the bases together to make a string

    # 500 BP random repetitive element
    motif2 = random.choices(bases, k=500) #500bp random sequence
    seq2 = "".join(motif2) #join the bases together to make a string

    # Write the repetitive elements to files - might be necessary/helpful to see the sequences for future analysis 
    with open("motif1.txt", "w") as f:
        f.write(seq)
    with open("motif2.txt", "w") as f:
        f.write(seq2)

    motifs = { 'motif1': seq, 'motif2': seq2 } #dictionary of the motifs


    num_insertions = [2, 3, 4, 5] #number of insertions to make

    ip = [] #list of insertion points
    mingenomelength = 1000000000000 #1 trillion, arbitrary maximum
    for m in os.listdir("Genomes"): #loop through files
        with open("Genomes/{}".format(m), "r") as f: #open files
            genomelength = f.read() #get length
            if genomelength < mingenomelength: #get shortest genome
                mingenomelength = genomelength
    for n in range(len(num_insertions)): #insert based on number of insertions
        ip.append(random.randint(0,mingenomelength)) #generate numbers that don't exceed the shortest genome

    for file in os.listdir("Genomes"): #loop through the genomes
        with open(f"Genomes/{file}", "r") as f:
            genome = f.read()

        accession = file.split(".")[0]

        for motif_name, sequence in motifs.items():
            for count in num_insertions: #loop through the number of insertions
                mod_genome = genome
                for i in range(count):
                    insertion_point = random.randint(0, len(mod_genome)) #randomly select a point in the genome to insert the repetitive element
                    mod_genome = mod_genome[:insertion_point] + sequence + mod_genome[insertion_point:]
                output_filename = f"{accession}_{motif_name}_{count}.fna"
                with open(f"Genomes/{output_filename}", "w") as out_f:
                    out_f.write(mod_genome)


# Joshua's Code - Running ART (Artificially Simulated Genomes)
def run_art():
    #original genomes list
    genomes = []
    for file in os.listdir("Genomes"):
        genomes.append(file)

    if not os.path.isdir("artgens"): #directory for simulated genomes
        os.system("mkdir artgens") #create directory if it doesn't exist
    os.chdir("artgens") #move to that directory

    for gen in genomes:
        #for depth in range(10,110,10): #increase depth from 10 to 100 in increments of 10
        for depth in [10,100]: #runs art with depth of 10 and 100
            out = str(gen.split("_")[0]) + "_" + str(gen.split("_")[1]) + "_" + str(depth)
            #art flags: -p = paired ends, -na = don't output alignment file, -i = input, -l = read length, -f = fold coverage, -o = output prefix, -m = mean fragment length, -s = standard deviation
            if not os.path.isfile("{}.fq".format(out)):
                os.system("art_illumina -p -na -i ../Genomes/{0} -l 151 -m 200 -s 10 -f {1} -o {2}".format(gen,depth,out))


# Kimia's Code - Running SPAdes and Unicycler
def run_spades():
    #directory to input files
    input_dir = "/home/project3/artgens"

    # SPAdes Run 
    #making output file
    output = "/home/project3/spades_output"
    os.makedirs(output, exist_ok=True)

    #read1 files in input directory 
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

def run_unicycler():
    # Unicycler Run 

    #making output file
    output_dir = "/home/project3/unicycler_output"
    os.makedirs(output_dir, exist_ok=True)

    #directory to input files
    input_dir = "/home/project3/artgens"

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

        #running unicycler
        subprocess.run(["unicycler", "-1", fq1_files_path, "-2", fq2_files_path, "-o", outdir1])
        print(f"unicycler finished")

# Call the functions in order
if __name__ == "__main__":
    download_genomes()
    generate_and_insert_repeats()
    run_art()
    run_spades()
    run_unicycler()

