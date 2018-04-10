# Genome Imager

Inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/8anoku/years_ago_i_wrote_a_java_application_which_draws/)
and [these](https://danielbiegler.github.io/visualize-dna-sequences/) [clones](https://bewelge.github.io/dnaSequenceVisualizer/)
([source](https://github.com/DanielBiegler/visualize-dna-sequences)/[source](https://github.com/Bewelge/dnaSequenceVisualizer))
I, relatively unskilled in python, set out on my first major project, a script that would visualize a DNA sequence in a graphical format.

And after a few hours of trial and error, frustrating debugging and frequent use of [stackoverflow](https://stackoverflow.com), it's done.

![Visualisation of Ebola Virus](https://raw.githubusercontent.com/logwet/genome-imager/master/Examples/ebola.png "Visualisation of Ebola Virus")

**Usage:**

1. Run the .exe
2. Or .py script (Python3 with PILLOW installed)
3. Specify the path of your DNA sequence file (.fasta recommended) *ie. path/to/file*
4. Done! A PNG image will be generated with the same name as the source data. *NOTE: Depending on the size of your source data, this process may be both time and memory consuming*

There are several sample files provided. `ebola.fasta`, `random.fasta`, which is a completely random DNA sequence, `otauri.fasta`, which is the DNA sequence of *Ostreococcus tauri* a species of green algae and `malaria_pathogen.fna` the genome of a pathogen that carries Human Malaria.
The Otauri and Malaria genomes are very large, and thus *will* take a long time to generate. I reccomend you run 64 bit Python with the Malaria genome because otherwise your computer *will* crash.

I stress that there is a hard limit as to how complex and large a genome you can render, namely processing power and most importantly available memory. This program indexes a *lot* of data into memory. For example, the malaria genome may use up in excess of 5 GB of memory while processing.

**Details:**

A (Adenine), T (Thymine), G (Guanine) and C (Cytosine) are represented with a green, red, pink and blue pixel and move the path up, down, left and right respectively. N (not-known) is a black pixel and doesn't move the path.

The start is represented by a golden circle and the end by a purple circle.

This project is not intended to be scientifically accurate in any way and should not be miscontrued for such. It is purely an aesthetic graphical representation. It is in now way actually representative of the real structure of the DNA vizualized.

-------------------------
Being a beginner, this script is undoubtedly filled with errors and unoptimized code. Please suggest improvements if you have any; particularly any regarding optimization and memory management.
