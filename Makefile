# SPDX-License-Identifier: GPL-3.0-only

OUTPUTS=\
	pcb-rpl-uph/local.pretty/MEC1521H_B0_I_TF.kicad_mod \
	pcb-rpl-uph/sym/MEC1521H_B0_I_TF.lib \
	build/RPL_UPH_FCBGA1744.check \
	pcb-rpl-uph/local.pretty/RPL_UPH_FCBGA1744.kicad_mod \
	pcb-rpl-uph/sym/RPL_UPH_FCBGA1744.lib

all: $(OUTPUTS)

build/RPL_UPH_FCBGA1744.check: pins/RPL_UPH_FCBGA1744/*.csv scripts/bga-check.py
	mkdir -p build
	./scripts/bga-check.py third-party/intel/cpu/rpl/hpu_ballout.csv pins/RPL_UPH_FCBGA1744
	touch $@

pcb-rpl-uph/local.pretty/%.kicad_mod: pins/%/*.csv scripts/bga-fp.py
	./scripts/bga-fp.py pins/$* $@

pcb-rpl-uph/sym/%.lib: pins/%/*.csv scripts/bga-sym.py
	./scripts/bga-sym.py pins/$* $@
