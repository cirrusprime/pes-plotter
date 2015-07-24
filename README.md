Need to add the path to the src directories to your PYTHONPATH.

For example on BASH, add this line to the .bashrc file:

export PYTHONPATH=~$PYTHONPATH:/path/to/pes-plotter/src/

Description of new directories:

bin - main executables of the code. 
      (1) Current central LLAMA script which calls all other modules
      (2) Standard plotting script (for basic graphs)

dev - directory to develop new code
      (1) 3D code and object oriented focus rewrite

examples - input files with corresponding graphs

src - same as obj for now. Should be all essential source code for mods

writing - latex docs for paper. some writing done
