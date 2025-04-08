import os 
import subprocess
import random 

# Joshua's Code - Downloading Genomes 
def download_genomes():
    if "Genomes" not in os.getcwd(): #if you aren't already in the Genomes folder
        if not os.path.isdir("Genomes"): #make a directory to store genomes if it doesn't already exist 
            os.system("mkdir Genomes")
        os.chdir("Genomes") #move to the Genomes folder

    accession = ["GCF_014961145.1","GCF_028532485.1","GCF_021391435.1","GCF_004379335.1"] # genome accession codes 

    for x in accession: #loop through accessions
        if x not in ",".join(os.listdir()): #no need to redownload 
            os.system(f"datasets download genome accession {x} --include genome") #download genome from refseq
            os.system("unzip ncbi_dataset.zip") #unzip
            os.system("rm ncbi_dataset.zip") #delete zip file which has generic name to prevent overwrite issues
            os.system("mv ncbi_dataset/data/GCF*/GCF* .") #extract the genome file and move it to current folder, which should be Genomes
            os.system("rm -rf ncbi_dataset/data") #delete the unzipped folder which has unnecessary extra stuff
            os.system("rm README.md") #delete extra file to avoid asking for overwrite
            os.system("rm md5sum.txt") #delete extra file to avoid asking for overwrite
            os.system("rmdir ncbi_dataset") #remove empty folder
    os.chdir("..") #return to main folder

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

    if not os.path.isdir("Motifs"): #make a directory to store the motifs if it doesn't already exist 
        os.system("mkdir Motifs")
        os.chdir("Motifs") #move to that directory
        # Write the repetitive elements to files - might be necessary/helpful to see the sequences for future analysis 
        with open("motif1.txt", "w") as f:
            f.write(seq)
        with open("motif2.txt", "w") as f:
            f.write(seq2)
        os.chdir("..") #move back to the original directory

    
    # Create a directory to store the modified genomes 
    modified_dir = "Modified_Genomes"
    if not os.path.isdir(modified_dir): #make a directory to store modified genomes if it doesn't already exist
        os.system(f"mkdir {modified_dir} ") #create directory if it doesn't exist
    
    # Create a dictionary of motifs
    motifs = {"motif1": seq, "motif2": seq2} 
    
    num_insertions = [2, 3, 4, 5] #number of insertions to make

    ip = [] #list of insertion points
    mingenomelength = 1000000000000 #1 trillion, arbitrary maximum
    for m in os.listdir("Genomes"): #loop through files
        with open("Genomes/{}".format(m), "r") as f: #open files
            dat = f.read() #get length
            genomelength = len(dat)
            if genomelength < mingenomelength: #get shortest genome
                mingenomelength = genomelength
    for n in range(len(num_insertions)+1): #insert based on number of insertions
        ip.append(random.randint(0,mingenomelength)) #generate numbers that don't exceed the shortest genome
    
    ip = sorted(ip) #sort the list of insertion points
    print(ip) #print the list of insertion points

    # Write the insertion points to a file - this is optional but can be helpful for debugging (able to check exact positions where the motifs were inserted)
    with open("Motifs/ip.txt", "w") as f:
        for i in ip:
            f.write(f"{i}\n")

    for file in os.listdir("Genomes"): #loop through the genomes
        with open(f"Genomes/{file}", "r") as f:
            genome = f.read()

        accession = file.split(".")[0]

        for motif_name, sequence in motifs.items():
            for count in num_insertions: #loop through the number of insertions
                mod_genome = genome
                for i in range(count):
                    insertion_point = ip[i] #iterate through the predetermined list of random insertion points based on the number of repeats
                    mod_genome = mod_genome[:insertion_point] + sequence + mod_genome[insertion_point:]
                output_filename = f"{accession}_{motif_name}_{count}.fna"
                
                with open(f"{modified_dir}/{output_filename}", "w") as out_f:
                    out_f.write(mod_genome)



# Joshua's Code - Running ART (Artificially Simulated Genomes)
def run_art():
    #original genomes list
    genomes = []
    for file in os.listdir("Modified_Genomes"):
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
                os.system("art_illumina -p -na -i ../Modified_Genomes/{0} -l 151 -m 200 -s 10 -f {1} -o {2}".format(gen,depth,out))


# Kimia's Code - Running SPAdes and Unicycler
def run_spades():
    #directory to input files
    input_dir = "artgens"

    # SPAdes Run 
    #making output file
    if not os.path.isdir("Spades_Output"): #make a directory to store SPAdes output if it doesn't already exist 
        os.system("mkdir Spades_Output") #create directory if it doesn't exist
    os.chdir("Spades_Output") #move to that directory


    #read1 files in input directory 
    fq_files_read1 = []
    for f in os.listdir(f"../{input_dir}"):
        if f.endswith('1.fq'):
            fq_files_read1.append(f)

    #run SPAdes for each file
    for fq1 in fq_files_read1:
        fq2 = fq1.replace('1.fq', '2.fq')

        fq1_path = f"../{input_dir}/{fq1}"
        fq2_path = f"../{input_dir}/{fq2}"

        #name for output
        base = fq1.replace('1.fq', '')
        outdir = f"{base}"
        os.system(f'mkdir {outdir}') #create directory for each output
       
        #run SPAdes with 2 threads
        os.system(f"spades.py -t 2 --only-assembler -1 {fq1_path} -2 {fq2_path} -o {outdir}") # Hillary's way 
        '''
        os.system("spades.py -t 2 --only-assembler -1 {0} -2 {1} -o Spades_Output".format(fq1_path, fq2_path)) # Josh's way 
        subprocess.run(["spades.py", "-1", fq1_path, "-2", fq2_path, "-o", "Spades_Output"]) # Kimia's way 
        # print(f"finish:{fq1} and {fq2} output in {outdir}")
        '''
    os.chdir('..') #move back to orginal direcotry 

def run_unicycler(): # MAKE CHANGES TO THIS FUNCTION 
    # Unicycler Run 

    #directory to input files
    input_dir = "artgens"

    #making output directory 
    if not os.path.isdir("Unicycler_Output"): #make a directory to store SPAdes output if it doesn't already exist 
        os.system("mkdir Unicycler_Output") #create directory if it doesn't exist
    os.chdir("Unicycler_Output") #move to that directory


    #forward read path
    fq1_files =[]
    for f in os.listdir(input_dir):
        if f.endswith('1.fq'):
            fq1_files.append(f)

    for fq1 in fq1_files:
        fq2 = fq1.replace('1.fq', '2.fq')

        fq1_path_un = f"../{input_dir}/{fq1}"
        fq2_path_un = f"../{input_dir}/{fq2}"

        base1 = fq1.replace('1.fq', '')
        outdir1 = f"{base1}"
        os.system(f'mkdir {outdir1}') #create directory for each output
    

        #running unicycler
        os.system(f"unicycler -t 2  -1 {fq1_path_un} -2 {fq2_path_un} -o {outdir1}")
        print(f"unicycler finished")


# Kimia's Code - Installing and running QUAST
def install_conda_and_quast():
    install_dir = "home/project3/quast/"
    miniconda_dir = miniconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    miniconda_script = os.path.join(install_dir, "Miniconda3-latest-Linux-x86_64.sh")

    os.makedirs(install_dir, exist_ok=True)

    #Downloadthe Miniconda
    subprocess.run(["wget", "-p", install_dir, miniconda_url])

    #conda environment
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "init", "bash"])
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "config", "--add", "channels", "defaults"])
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "config", "--add", "channels", "bioconda"])
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "config", "--add", "channels", "conda-forge"])
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "update", "conda", "-y"])


    #update conda
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "update", "conda", "-y"])

    #create environment
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "create", "-n", "compbio", "python=3.9", "-y"])

    #install quast
    subprocess.run([f"{install_dir}/miniconda3/bin/conda", "run", "-n", "compbio", "install", "-c", "bioconda", "quast", "-y"])
    print("Installation complete")


# Call the functions in order
if __name__ == "__main__":
    download_genomes()
    generate_and_insert_repeats()
    run_art()
    run_spades()
    run_unicycler()
    install_conda_and_quast()