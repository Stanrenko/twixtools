# twixzip</span>.py Installation & Usage

## Purpose

twixzip is a Python based command line tool for Siemens MRI raw data compression. Following compression methods can be selected via the command line:

* Oversampling removal
* Lossy floating point compression using the zfp library
* Single coil compression (scc) based on singular value decomposition (SVD)
* Geometric coil compression (gcc) based on SVD
* Optionally FID navigators can be removed

Before applying the selected compression method(s), lossless compression (gzip) is applied to the header and meta data information which is then added to a hdf5 file. All additional meta information necessary for decompression (e.g. coil compression matrices) are also stored in the hdf5 file.

## Installation

Navigate to the twixtools folder in an open terminal and install twixzip</span>.py with pip:

    pip install .

Installation through python setup</span>.py install is currently not possible.

## Requirements

The tool works under Python 3.7 with the following packages installed:

* numpy &ge; 1.17.3
* pyzfp &ge; 0.3.1
* pytables &ge; 3.6.1

The pyzfp and pytables libraries can be installed via pip:

    pip install pyzfp
    pip install tables

## Usage

Executing the command twixzip</span>.py in an open terminal gives an overview of all possible arguments. Optional arguments are:

    -h:  help  
    -d:  decompress data

Input and output directories & filenames are required arguments that can be selected via:

    -i infile:  input file  
    -o outfile: output file

In the compression mode the input file should be an MRI raw data file, in the decompression mode (`-d`) it should be the hdf5 file containing the compressed data. The output file is then an hdf5 file (compression mode) or an MRI raw data file (decompression mode).

Compression methods can be selected via:

    --remove_fidnav:            removes FID navigators  
    --remove_os:                removes oversampling
    --scc -n NCC:               single coil compression (SCC) - keep NCC virtual coils
    --scc -t CC_TOL:            SCC - number of coils is calculated with a tolerance for the singular values
    --scc_bart -n NCC:          SCC using BART  
    --gcc -n NCC:               geometric coil compression (GCC) - keep NCC virtual coils
    --gcc -t CC_TOL:            GCC - number of coils is calculated with a tolerance for the singular values
    --gcc_bart -n NCC:          GCC using the Berkeley Advanved Reconstruction Toolbox (BART) [1]         
    --zfp --zfp_tol ZFP_TOL:    floating point compression with ZFP_TOL tolerance
    --zfp --zfp_prec ZFP_PREC:  floating point compression with ZFP_PREC precision (not recommended)

The optional argument `--testmode` can be used to automatically decompress the data after compression. The created decompressed MRI raw data filename contains the selected compression method. The option `--profile` can be used to profile the compression code.

[1] BART Toolbox for Computational Magnetic Resonance Imaging, DOI: 10.5281/zenodo.592960