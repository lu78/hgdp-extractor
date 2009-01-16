
help:
	echo "I hate writing makefiles!!!'
	echo "this makefiles is valid only to extract one continent_macroarea at the time"

CHROMOSOMES =1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y
BASEDIR = '/home/gioby/' 
RESULTSDIR = BASEDIR + Data/HGDP/Results
RESULTSFILES = $(addprefix $(RESULTSDIR)/chr, $(addsuffix _filtered.txt, $(CHROMOSOMES)))


all: $(RESULTSFILES)

$(RESULTSDIR)/chr%_filtered.txt: 
	
#	echo $(findstring ch%o, chdsado, ch%o)
#	@echo "I hate makefiles"
	@echo $*
	-python src/hgdp_snp_extractor.py -c Europe -y $*

