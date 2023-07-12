OUTPUTS=\
	pcb-rpl-uph/local.pretty/RPL_UPH_FCBGA1744.kicad_mod \
	pcb-rpl-uph/sym/RPL_UPH_FCBGA1744.lib

all: $(OUTPUTS)

pcb-rpl-uph/local.pretty/%.kicad_mod: pins/%.csv scripts/bga-fp.py
	./scripts/bga-fp.py $< $@

pcb-rpl-uph/sym/%.lib: pins/%.csv scripts/bga-sym.py
	./scripts/bga-sym.py $< $@
