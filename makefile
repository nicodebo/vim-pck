GREPPRG=ag
TAGPRG=ctags
TEST=pytest
ENV_TEST=tox
ZCOMPDIR=~/.config/zsh/zcompletion/
COMPFILE=_vimpck
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


tags:
	$(GREPPRG) -l | $(TAGPRG) --links=no -L-

sym_comp:
	ln -sf $(ROOT_DIR)/completion/$(COMPFILE) $(ZCOMPDIR)/$(COMPFILE)

clean_comp:
	rm ${ZCOMPDIR}/$(COMPFILE)

mrproper: clean_comp
