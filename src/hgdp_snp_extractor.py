#!/usr/bin/env python
# Copyright GPL 3.0 Giovanni Dall'Olio
"""
Extract SNPs from a HGDP SNP file.     #TODO: refactore everything!! 

To parse the files, it uses the libraries on Gio.HGDP from the experimental
biopython popgen module. 

usage:
    python hgdp_snp_extractor.py 
            [--samplesfile '/home/gioby/Data/HGDP/Annotations/samples_subset.csv']
            [--genotypes_by_chr_dir  /home/gioby/Data/HGDP/Genotypes_by_chr/]
            --chromosome 22    [default 22]
            --continents Europe    [default Europe]
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

def get_parameters():
    """Read arguments and parameters
    
    input:
    - [samplesfile] -> description of sample file
    - [genotypes_by_chr_dir]
    - chromosomes   [22]
    - continent     [Europe]
    - [outputfile]

    output:
    - samples_filter -> a list of individuals id to be filtered 
            (belonging to the same continent)
    - genotypes_file path
    - output file path 
    """
    
    basedir = '/home/gioby/Data/HGDP/'
    
    # parse parameters
    parser = OptionParser()
    
    parser.set_defaults(genotypes_by_chr_dir = basedir + 'Genotypes_by_chr/',
                        samplesfilepath = basedir + 'Annotations/samples_subset.csv',
                        selected_chr = 22,  # only a chromosome per run
                        continent = 'Europe')
    
    parser.add_option('-s', '--samplefile', action='store', type='string', 
                      dest = 'samplesfilepath')
    parser.add_option('-g', '--genotypes_by_chr_dir', action='store', 
                      type='string', dest = 'genotypes_by_chr_dir')
    parser.add_option('-c', '--continent', action='store', type='string', 
                      dest = 'continent')
    parser.add_option('-y', '--chromosomes', action='store', type='string', 
                      dest = 'chrom', default='22')
    parser.add_option('-o', '--outputfile', action='store', type='string', 
                      dest = 'outputfile')
    parser.add_option('-t', '--test', action='callback', callback=test_europe_extract, nargs=0)
    
    (options, args) = parser.parse_args()

    genotypesfile = options.genotypes_by_chr_dir + '/chr' + options.chrom + '.geno' 
                       
    logging.debug(genotypesfile)

    outputfile = basedir + 'Results/hgdp_chr%s_%s.geno' %(options.chrom, 
                                                          options.continent)

    # get a list of individuals (samples) belonging to the continent
    samples_filter = get_samples_list(options.samplesfilepath, options.continent)
    return samples_filter, genotypesfile, outputfile

def get_samples_list(samplesfilepath, continent):
    """Read Samples File and take the IDs of the samples to be filtered 
    (actually it filters by continent)
    """
    samplesfile = open(samplesfilepath, 'r')
    samples = hgdpsamplesfileParser(samplesfile)
    samples_filter = [sample.individual_id for sample in samples if sample.continent == continent]
    print samples_filter
    return samples_filter
    
#    return samples_filter, genotypes_files, outputfile

def getFilteredGenotypes(samples_filter, genotypesfilename):
    """Read a Genotypes File and selects all the genotypes belonging to a population
    
    """

    genotypefile = open(genotypesfilename, 'r')
    logging.debug(genotypefile)
    markers = hgdpgenotypesParser(genotypefile, samples_filter)
    return markers

def printGenotypes(markers, outputfile):
    """
    print the genotypes to an output file
    """
    output = ''
    
    # add header
    output = '\t' + ' '.join([ind.name for ind in markers]) + '\n'
    logging.debug('Markers:')
    logging.debug(markers)
    
    # add genotypes
    for marker in markers:
        output += marker.to_geno_format() + '\n'
        
#            print marker.genotypes
#            print marker.individuals

    logging.debug(output)
    out = open(outputfile, 'w')
    out.write(output)
    out.close()
    print 'saved to ', outputfile
 

def test_europe_extract(*args):
    """Test the extraction of European individuals on Chromosome 1 from a sample file

    Note: use nose to run tests.
    """
#    print 'args ', args

#    logging.basicConfig(level = logging.DEBUG)
    import doctest
    doctest.testmod()

    basedir = '/home/gioby/Data/HGDP/'
#    testgenotypefile = [basedir + 'Test/chr22_100.geno', ]
    testgenotypefile = basedir + 'Test/chr1_30.geno'

#    [samplesfilter, genotypes_files, outputfile] = get_parameters() TODO: don't call get_parameters twice
    continent = 'Europe'
    samplesfilepath = basedir + '/Annotations/samples_subset.csv'

    samples_filter =  get_samples_list(samplesfilepath, continent)
    
    samples = getFilteredGenotypes(samples_filter, testgenotypefile)
    outputfile = basedir + 'Results/test.europe' 

#    logging.debug(pformat(samples_filter)) 

    printGenotypes(samples, outputfile)
    sys.exit()
     
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(funcName)s - %(lineno)d - %(message)s")
    [samples_filter, genotypes_files, outputfile] = get_parameters()

    samples = getFilteredGenotypes(samples_filter, genotypes_files)
    logging.debug(samples)
    printGenotypes(samples, outputfile)
    
