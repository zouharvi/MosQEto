LATEX=pdflatex
MAINFILE=report

default: $(MAINFILE).pdf

$(MAINFILE).pdf: references.bib

%.pdf: %.tex
	$(LATEX) $<
	bibtex $* || ( echo "Bibtex failed" && exit 1 )
	# change the exit 1 to exit 0 in the line above if you want to ignore it
	lim=4; \
	  while [ $$lim -ge 0 ] \
	      && grep 'Rerun to get\|Citation.*undefined' $*.log >/dev/null 2>/dev/null; do \
	    $(LATEX) $< ; \
	    lim=$$(($$lim - 1)) ; \
	  done

.PHONY: ci
ci:
	# make sure git will remember my password
	git config credential.helper store
	# git pull push dance with possibly uncommited local modifications
	if git pull; then echo No changes to hide; else git stash; git pull; git stash apply; fi; git commit -am "make ci by $(USER)"; git push

clean:
	rm -f $(MAINFILE).log $(MAINFILE).aux $(MAINFILE).bbl $(MAINFILE).blg $(MAINFILE).toc $(MAINFILE).out $(MAINFILE).run.xml $(MAINFILE).bcf
