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

def parameters():
    basedir = '/home/gioby/Data/HGDP/'
    samplesfile = file(basedir + 'Annotations/samples_subset.csv', 'r')
    genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/'
    selected_chr = [22,]
    genotypes_files = [genotypes_by_chr_dir + '/chr' + str(chrom) + '.geno' 
                       for chrom in selected_chr]
    logging.debug(genotypes_files)
    continent = 'Europe'
    
    # Read Samples File
    samples = hgdpsamplesfileParser(samplesfile)
    samples_filter = [sample for sample in samples if sample.continent == continent]
    
    return samples_filter, genotypes_files 

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

def printGenotypes(markers_by_chr):
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
 

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
#    logging.basicConfig(level = logging.DEBUG)
    [samples_filter, genotypes_files] = parameters()
    logging.debug(pformat(samples_filter)) 
    
    basedir = '/home/gioby/Data/HGDP/'
    testgenotypefile = [basedir + 'Test/chr1_100.geno', ]
    testgenotypefile = [basedir + 'Test/chr1_30.geno', ]
    
    samples = getFilteredGenotypes(samples_filter, testgenotypefile)
    printGenotypes(samples)
