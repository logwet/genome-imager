# Genome Imager

Inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/8anoku/years_ago_i_wrote_a_java_application_which_draws/)
and [these](https://danielbiegler.github.io/visualize-dna-sequences/) [clones](https://bewelge.github.io/dnaSequenceVisualizer/)
([source](https://github.com/DanielBiegler/visualize-dna-sequences)/[source](https://github.com/Bewelge/dnaSequenceVisualizer))
I, relatively unskilled in python, set out on my first major project, a script that would visualize a DNA sequence in a graphical format.

And after a few hours of trial and error, frustrating debugging and frequent use of [stackoverflow](https://stackoverflow.com), it's done.

**Usage:**

1. Run the .exe
2. Or .py script (Python3 with PILLOW installed)
3. Specify the path of your DNA sequence file (.fasta recommended) *ie. path/to/file.fasta*
4. Done! A PNG image will be generated with the same name as the source data. *NOTE: Depending on the size of your source data, this process may be both time and memory consuming*

There are several sample .fasta files provided. `ebola.fasta`, `random.fasta`, which is a completely random DNA sequence and `otauri.fasta`, which is the DNA sequence of *Ostreococcus tauri*, a species of green algae.
#### Details:

A (Adenine), T (Thymine), G (Guanine) and C (Cytosine) are represented with a green, red, pink and blue pixel and move the path up, down, left and right respectively. N (not-known) is a black pixel and doesn't move the path.

The start is represented by a golden circle and the end by a purple circle.

This project is not intended to be scientifically accurate in any way and should not be miscontrued for such. It is purely an aesthetic graphical representation. It is in now way actually representative of the real structure of the DNA vizualized.

-------------------------
Being a beginner, this script is undoubtedly filled with errors and unoptimized code. Please suggest improvements if you have any; particularly any regarding optimization and memory management.
