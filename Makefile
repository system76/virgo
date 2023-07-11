all: pcb-motherboard/local.pretty/RPL_UPH_FCBGA1744.kicad_mod

pcb-motherboard/local.pretty/%.kicad_mod: pins/%.csv
	./scripts/bga-fp.py $< $@
