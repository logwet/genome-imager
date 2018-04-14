# Genome Imager

Inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/8anoku/years_ago_i_wrote_a_java_application_which_draws/)
and [these](https://danielbiegler.github.io/visualize-dna-sequences/) [clones](https://bewelge.github.io/dnaSequenceVisualizer/)
([source](https://github.com/DanielBiegler/visualize-dna-sequences)/[source](https://github.com/Bewelge/dnaSequenceVisualizer))
I, relatively unskilled in python, set out on my first major project, a script that would visualize a DNA sequence in a graphical format.

And after a lot of work, frustrating debugging and frequent use of [stackoverflow](https://stackoverflow.com), it's done.

![Visualisation of Ebola Virus](https://raw.githubusercontent.com/logwet/genome-imager/master/Examples/ebola.png "Visualisation of Ebola Virus")

**Usage:**

- *Run this program in a 64 bit version of Python! A 32 bit version is only able to access 4 GB of memory, which is far too little to run this program
If you don't have a 64 bit version of Python, a 64 bit `.exe` is provided for Windows users.*
- Call the program from the command line: `python3 genome-imager.py path/to/file <args>`
- Or `genome-imager.exe path/to/file <args>`
- A PNG image will be generated with the same name as the source data. *NOTE: Depending on the size of your source data, this process may be both time and memory consuming*

There are several sample files and their resulting images in the `Examples` folder:
- `ebola.fasta` - Genome of the Ebola Virus
- `hiv.fna` - Genome of the HIV virus
- `random.fasta` - Randomly generated genetic sequence - 10000 characters
- `random2.fasta` - Randomly generated genetic sequence - 1000000 character
- `otauri.fasta` - Genetic sequence of *Ostreococcus tauri* a species of green algae
- `malaria_pathogen.fna` - Genome of *Plasmodium falciparum* a pathogen that carries Human Malaria

The Otauri and Fruit Fly genomes are large, and thus will take some time to generate.

I have actually amassed a large collection of genomes and rendered quite a few of them, but because of the limitations of `git` and GitHub I cannot store them here.
I have put them all into a [Google Drive folder](https://drive.google.com/open?id=1yryCHJsiteDRuPLq6spoyHxDkzimhmWP), which will be updated as I get more genomes. Read `contents.txt` in the folder for more information.

~~I stress that there is a hard limit as to how complex and large a genome you can render, namely processing power and most importantly available memory. This program indexes a *lot* of data into memory and will likely dip into your page file with larger genomes.~~

Recently, I've implemented a mechanism that automatically dumps (compressed) Memory onto the disk in the form of temp files, keeping the program's total memory usage low. This can be tweaked by passing a `--dump-size` argument to the program (See `genome-imager.py help` for more information.)

Despite this, there is still a limit of around 450 MB for input files on a machine with 8 GB of RAM. Any higher and there is a possibility you will run into a `MemoryError`

**Details:**

A (Adenine), T (Thymine), G (Guanine) and C (Cytosine) are represented with a green, red, pink and blue pixel and move the path up, down, left and right respectively. N (not-known) is a black pixel and doesn't move the path.

The start is represented by a yellow circle and the end by a light blue circle.

This project is not intended to be scientifically accurate in any way and should not be miscontrued for such. It is purely an aesthetic graphical representation. It is in now way actually representative of the real structure of the DNA.

-------------------------
I want to optimize this program to the extent that it can handle input files over a gigabyte, maybe even the human genome in the future. Please suggest improvements if you have any; particularly any regarding optimization and memory management of PIL.
