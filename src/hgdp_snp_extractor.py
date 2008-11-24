#!/usr/bin/env python
# Copyright GPL 3.0 Giovanni Dall'Olio
"""
Extract SNPs from a HGDP SNP file. 

usage:
    python hgdp_snp_extractor.py 
            [--samplesfile '/home/gioby/Data/HGDP/Annotations/samples_subset.csv']
            [--genotypes_by_chr_dir  /home/gioby/Data/HGDP/Genotypes_by_chr/]
            --chromosomes 22    [default 22]
            --continents European    [default European]
            [--outputfile /home/gioby/Data/HGDP/Results/european_chr22.geno]
            
"""

from PopGen.Gio.HgdpIO import hgdpgenotypesParser, hgdpsamplesfileParser
from pprint import pprint, pformat
import logging
import os
import getopt
from optparse import OptionParser
import sys

def usage():
    """ """
    print __doc__
    sys.exit()

def parameters():
    # Read arguments and parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "ht", ["help", "test", "samplefile=", "genotypes_by_chr_dir=",
                                          "chromosomes=", "continent=", "outputfile="])

    except getopt.GetoptError, err:
        usage()

    if opts == []:
        usage()
        
    samplesfile = ''
    genotypes_by_chr_dir = ''
    selected_chr = []
    continent = ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('--test', '-t'):
            _test()
        elif opt in ('--samplesfile', '-s'):
            samplesfile = arg
        elif opt in ('--window', '-w'):
            sliding_windows_file_path = arg
        elif opt in ('--output', '-o'):
            output_file_path = arg
        

    # TODO: getopt interface
    basedir = '/home/gioby/Data/HGDP/'
    if samplesfile == '':    
        samplesfile = file(basedir + 'Annotations/samples_subset.csv', 'r')
    if genotypes_by_chr_dir == '':
        genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/'
    if selected_chr == []:
        selected_chr = [22, ]
    if continent == '':
        continent = 'Europe'
        
    genotypes_files = [genotypes_by_chr_dir + '/chr' + str(chrom) + '.geno' 
                       for chrom in selected_chr]
    logging.debug(genotypes_files)
#    continent = 'Asia'
    outputfile = basedir + 'Results/hgdp_chr22_' + continent + '.geno'
    
    # Read Samples File
    samples = hgdpsamplesfileParser(samplesfile)
    samples_filter = [sample for sample in samples if sample.continent == continent]
    
    return samples_filter, genotypes_files, outputfile

def getFilteredGenotypes(samples_filter, genotypes_files):
    # Read Genotypes File, filtering by population
    markers_by_chr = {}
    for genotypesfilename in genotypes_files:
        try:
            genotypefile = file(genotypesfilename, 'r')
            logging.debug(genotypefile)
        except:
            raise ValueError("Could not open file %s" % genotypesfilename)
        
        markers_by_chr[genotypesfilename] = hgdpgenotypesParser(genotypefile, samples_filter)
    return markers_by_chr

def printGenotypes(markers_by_chr, outputfile):
    output = ''
    
    for chrom in markers_by_chr:
        # add header
        output = '\t' + ' '.join([ind.individual_id for ind in markers_by_chr[chrom][0].individuals]) + '\n'
        
        # add genotypes
        for marker in markers_by_chr[chrom]:
            output += marker.to_geno_format() + '\n'
            
#            print marker.genotypes
#            print marker.individuals

    print output
    out = file(outputfile, 'w')
    out.write(output)
    out.close()
 

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
#    logging.basicConfig(level = logging.DEBUG)
    [samples_filter, genotypes_files, outputfile] = parameters()
    logging.debug(pformat(samples_filter)) 
#    print outputfile
    test = 0
    
    if test:
        basedir = '/home/gioby/Data/HGDP/'
        #    testgenotypefile = [basedir + 'Test/chr1_100.geno', ]
        testgenotypefile = [basedir + 'Test/chr1_30.geno', ]
    
        samples = getFilteredGenotypes(samples_filter, testgenotypefile)
    else:
        samples = getFilteredGenotypes(samples_filter, genotypes_files)
    printGenotypes(samples, outputfile)
