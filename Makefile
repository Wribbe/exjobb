DIR_STATIC := exjobb/webapp/static
DIR_REPORTS := ${DIR_STATIC}/pdf/reports
DIR_DIFF := msccls/diff
DIR_CLONE := exjobb_at_revision

URL_GIT := $(shell git remote get-url origin)

PATH_FIGURES=msccls/figures
FIGUTILS:=$(wildcard msccls/figures/utils/*.py)
PY:=virt_py3/bin/python

figures_py=$(foreach d,$(filter-out %__.py,$(wildcard ${PATH_FIGURES}/*.py)),${d:%.py=%.pdf})
figures_pyx=$(foreach d,$(wildcard ${PATH_FIGURES}/*.pyx),${d:%.pyx=%.pdf})
figures=${figures_py} ${figures_pyx}

pdflatex=pdflatex -interaction=nonstopmode
deps_tex=$(filter-out %report.tex,$(wildcard msccls/*.tex))

NOW := $(shell date '+%Y-%m-%d_%H:%M:%S')
REPORT_TEMP := report.tex.temp

DEPS_ALL := \
	msccls/preface.pdf ${DIR_STATIC}/report.pdf msccls/toc.guard ${figures} \
#	msccls/diff/diff.pdf

#all: ${DEPS_ALL}
#	[ ! -f "msccls/${REPORT_TEMP}" ] || mv msccls/${REPORT_TEMP} msccls/report.tex

all: ${DEPS_ALL}

virt_py3: requirements.txt
	rm -rf $@
	python -m venv $@
	$@/bin/python -m pip install --upgrade pip
	$@/bin/python -m pip install -r $^

${DIR_CLONE}/%:
	git clone ${URL_GIT} ${DIR_CLONE}
	cd ${DIR_CLONE} && git checkout revision && make

msccls/report.bbl : msccls/report.bib
	cd msccls && ${pdflatex} report && biber report && ${pdflatex} report

msccls/toc.guard : msccls/report.tex
	[ -z "$(shell diff -q $@ msccls/report.toc)" ] || { cd msccls && ${pdflatex} report.tex; }
	cat msccls/report.toc > msccls/toc.guard

${DIR_DIFF}/diff.tex : ${DIR_DIFF}/report_base.tex ${DIR_DIFF}/report.tex
	#latexdiff --enable-citation-markup --append-textcmd="enumerate" $^ > $@
#	latexdiff --enable-citation-markup --append-safecmd="begin" $^ > $@
	#latexdiff --enable-citation-markup --append-safecmd="begin" --exclude-safecmd="todo" --allow-spaces --append-mboxsafecmd="begin" --config="PICTUREENV=(?:picture|DIFnomarkup|description)[\w\d*@]*" $^ > $@
#	latexdiff --exclude-safecmd="todo" --append-textcmd="begin" --allow-spaces --enable-citation-markup --config="PICTUREENV=(?:picture|DIFnomarkup|description|quote|enumerate)[\w\d*@]*" $^ > $@
	latexdiff --append-safecmd="subsection,section" --exclude-safecmd='ldots' --config="PICTUREENV=(?:picture|DIFnomarkup|enumerate|itemize|quote)[\w\d*@]*" $^ > $@
#	latexdiff --append-safecmd="subsection,section,begin\{quote\}" --exclude-safecmd='ldots' $^ > $@
${DIR_DIFF}/diff.pdf : ${DIR_DIFF}/diff.tex msccls/diff.bbl msccls/diff.bcf msccls/diff.bib msccls/diff.blg
	cp $(filter %.tex,$^) msccls/ && cd msccls && ${pdflatex} diff.tex && cp diff.pdf ../${DIR_DIFF}
	rm msccls/diff.tex
	cp $@ ${DIR_DIFF}/${NOW}_diff.pdf

${DIR_DIFF}/report.tex : msccls/report.tex | ${DIR_DIFF}
	cd msccls && latexpand report.tex > ../$@
	python tex_strip_unwanted.py $@

${DIR_DIFF}/report_base.tex : ${DIR_CLONE}/msccls/report.tex | ${DIR_DIFF}
	cd ${DIR_CLONE}/msccls && latexpand report.tex > ../../$@
	python tex_strip_unwanted.py $@

${DIR_STATIC}/report.pdf : msccls/report.tex ${figures} ${deps_tex} msccls/report.bbl | ${DIR_REPORTS}
	cd msccls && ${pdflatex} report.tex && cp report.pdf ../$@
	# Remove other same-day pdfs.
	rm -rf ${DIR_REPORTS}/$(shell date '+%Y-%m-%d_')*.pdf
	# Copy report.pdf to timestamped report.
	cp $@ ${DIR_REPORTS}/${NOW}_report.pdf

${DIR_REPORTS}, ${PATH_FIGURES}, ${DIR_REPORTS} :
	mkdir -p $@

${PATH_FIGURES}/%.pdf : ${PATH_FIGURES}/%.py csv_to_pdf.py ${FIGUTILS} | ${PATH_FIGURES} virt_py3
	${PY} csv_to_pdf.py ${@:%.pdf=%.py} $@

${PATH_FIGURES}/%.pdf : ${PATH_FIGURES}/%.pyx | ${PATH_FIGURES}
	${PY} $^ $@

clean:
	rm -rf ${PATH_FIGURES} ${PATH_FIGURES_DATA}

#${DIR_STATIC}/report.pdf : msccls/preface.pdf

msccls/preface.pdf : msccls/preface.tex | virt_py3
	cd msccls && ${pdflatex} preface.tex

${DIR_DIFF} :
	mkdir $@

diff:
	rm -rf ${DIR_DIFF}
	$(MAKE)

msccls/diff.% : msccls/report.%
	cp $^ $@

.PHONY: all clean diff
