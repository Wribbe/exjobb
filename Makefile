DIR_STATIC=exjobb/webapp/static
DIR_REPORTS=${DIR_STATIC}/pdf/reports

all: ${DIR_STATIC}/report.pdf msccls/toc.guard msccls/report.aux

msccls/report.aux : msccls/report.bib
	cd msccls && pdflatex report 1>/dev/null && bibtex report && pdflatex report 1>/dev/null

msccls/toc.guard : msccls/report.tex
	[ -z "$(shell diff -q $@ msccls/report.toc)" ] || { cd msccls && pdflatex report.tex; }
	cat msccls/report.toc > msccls/toc.guard

${DIR_STATIC}/report.pdf : msccls/report.tex msccls/report.aux | ${DIR_REPORTS}
	cd msccls && pdflatex report.tex 1>/dev/null && cp report.pdf ../$@
	# Remove other same-day pdfs.
	rm -rf ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_')*.pdf
	# Copy report.pdf to timestamped report.
	cp $@ ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_%H:%M:%S')_report.pdf

${DIR_REPORTS} :
	mkdir -p $@

.PHONY: all
