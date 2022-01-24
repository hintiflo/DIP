# Beschreibung:	Makefile fuer ein LaTeX Projekt
# Autor:				Sebastian Stein <seb.stein@hpfsc.de>
# Datum:				2004/03/03 22:07:00 Mit
# legt das Suffix der zentralen tex Datein fest, also z. B. index.tex
#
# In dieser Datei werden alle Einstellungen fuer das Projekt vorgenommen.
# Weiterhin werden in dieser Datei die einzelnen Kapitel in der richtigen
# Reihenfolge reingehaengt. Fuer jedes Kapitel sollte eine eigene tex Datei
# angelegt werden.
#
# Beispiel: ZENTRAL_TEX = index
ZENTRAL_TEX = Bakk

# zentrale Regeln für die DVI Erstellung
$(ZENTRAL_TEX).dvi: $(ZENTRAL_TEX).toc $(ZENTRAL_TEX).blg $(ZENTRAL_TEX).bbl
	pdflatex $(ZENTRAL_TEX)

# fuer Inhaltsverzeichnis und Vorbereitung Literaturverzeichnis
$(ZENTRAL_TEX).aux $(ZENTRAL_TEX).toc: $(ZENTRAL_TEX).tex
	pdflatex $(ZENTRAL_TEX)

# Literaturliste erstellen
$(ZENTRAL_TEX).blg $(ZENTRAL_TEX).bbl: $(ZENTRAL_TEX).aux 
# $(ZENTRAL_TEX).bib
	bibtex $(ZENTRAL_TEX)
	$(MAKE)

# Index/Stichwortverzeichnis erstellen
index:
	makeindex -g -s index.ist $(ZENTRAL_TEX)

# RTF erstellen
rtf:
	latex2rtf $(ZENTRAL_TEX)

# Index/Stichwortverzeichnis erstellen
stichwort:
	$(MAKE) index

# Glossar erstellen
glossar:
	makeindex index.glo -s nomencl.ist -o index.gls

# HTML mittels latex2html erzeugen
html:
	echo "\usepackage{german}" > l2h.tex
	latex2html -noinfo -image_type png -accent_images png -show_section_numbers -dir html -mkdir -up_url "../index.html" -up_title "Zur Startseite" -local_icons index.tex
	./tidy.sh
	rm html/*.pl
	rm html/images.*
	rm html/WARNINGS
	cat html/index.html | sed -e "s/emergenz@hpfsc.de/emergenz-AT-hpfsc.de/" > html/tmp
	mv html/tmp html/index.html
	echo "" > l2h.tex

# alle Dateien loeschen, die von latex automatisch erzeugt werden;
clean:
	rm -f $(ZENTRAL_TEX).dvi
	rm -f $(ZENTRAL_TEX).lot
	rm -f $(ZENTRAL_TEX).out
	rm -f $(ZENTRAL_TEX).lot
	rm -f $(ZENTRAL_TEX).ps
	rm -f $(ZENTRAL_TEX).pdf
	rm -f $(ZENTRAL_TEX).rtf
	rm -f $(ZENTRAL_TEX).aux
	rm -f $(ZENTRAL_TEX).bbl
	rm -f $(ZENTRAL_TEX).blg
	rm -f $(ZENTRAL_TEX).idx
	rm -f $(ZENTRAL_TEX).ilg
	rm -f $(ZENTRAL_TEX).ind
	rm -f $(ZENTRAL_TEX).log
	rm -f $(ZENTRAL_TEX).toc
	rm -Rf html/

# fuehrt aspell auf alle tex Dateien ausser auf die zentrale tex Datei, da dort
# hauptsaechlich tex Befehle sind und aspell nur viele Falschwarnungen
# produziert
aspell:
	@liste=`ls *.tex`; \
	for tex in $$liste;  \
	do  \
		if [ $$tex != "$(ZENTRAL_TEX).tex" ]; then  \
			echo "aspell -t -x -c $$tex" ;  \
			aspell -t -x -c $$tex ; \
		fi ; \
	done

# ruft die Rechtschreibpruefung durch aspell auf
spell:
	$(MAKE) aspell

# ruft die Rechtschreibpruefung durch aspell auf
rechtschreibung:
	$(MAKE) aspell
