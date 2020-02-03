DIR_STATIC=exjobb/webapp/static
DIR_REPORTS=${DIR_STATIC}/pdf/reports

PATH_FIGURES_DATA=msccls/data_figures
PATH_FIGURES=msccls/figures

figures=$(foreach d,\
	$(wildcard ${PATH_FIGURES_DATA}/*.csv), \
	$(subst ${PATH_FIGURES_DATA},${PATH_FIGURES},${d:%.csv=%.pdf}) \
)

#all: ${DIR_STATIC}/report.pdf msccls/toc.guard msccls/report.aux ${figures}
all: ${DIR_STATIC}/report.pdf msccls/toc.guard msccls/report.aux ${figures}
	echo ${figures}

msccls/report.aux : msccls/report.bib
	cd msccls && pdflatex report && bibtex report && pdflatex report

msccls/toc.guard : msccls/report.tex
	[ -z "$(shell diff -q $@ msccls/report.toc)" ] || { cd msccls && pdflatex report.tex; }
	cat msccls/report.toc > msccls/toc.guard

${DIR_STATIC}/report.pdf : msccls/report.tex msccls/report.aux ${figures} | ${DIR_REPORTS}
	cd msccls && pdflatex report.tex && cp report.pdf ../$@
	# Remove other same-day pdfs.
	rm -rf ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_')*.pdf
	# Copy report.pdf to timestamped report.
	cp $@ ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_%H:%M:%S')_report.pdf

${DIR_REPORTS}, ${PATH_FIGURES} :
	mkdir -p $@

${PATH_FIGURES}/%.pdf : ${PATH_FIGURES_DATA}/%.csv csv_to_pdf.py sync_db.py | ${PATH_FIGURES}
	python csv_to_pdf.py $(filter %.csv,$^) $@

clean:
	rm -rf ${PATH_FIGURES} ${PATH_FIGURES_DATA}

.PHONY: all clean
