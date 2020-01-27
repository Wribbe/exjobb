DIR_STATIC=exjobb/webapp/static
DIR_REPORTS=${DIR_STATIC}/pdf/reports

all: ${DIR_STATIC}/report.pdf

${DIR_STATIC}/report.pdf : msccls/report.tex | ${DIR_REPORTS}
	cd msccls && pdflatex report.tex && cp report.pdf ../$@
	# Remove other same-day pdfs.
	rm -rf ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_')*.pdf
	# Copy report.pdf to timestamped report.
	cp $@ ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_%H:%M:%S')_report.pdf

${DIR_REPORTS} :
	mkdir -p $@
