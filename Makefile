PSCAD=./pscad.py

SRC=\
	dip-32.pscad \
	KK100-3.pscad \
	45558-0003.pscad \
	HEADER_2MM_2x1.pscad \
	HEADER_2MM_2x3.pscad \
	HEADER_2MM_3x6.pscad \
	PowerPAK_SO-8.pscad \
	pcie_x1.pscad \
	pcie_x4.pscad \
	pcie_x8.pscad \
	pcie_x16.pscad \
	xilinx_jtag.pscad \
	ti_jtag.pscad \
	1204-4.pscad \
	2010-4.pscad \
	2412-4.pscad \
	1224-4.pscad \
	ddr2_clp.pscad \
	FF784.pscad \
	onfi_bga100.pscad \
	PTD08A010W.pscad \
	PTD08A020W.pscad \
	PTD08A0X0W.pscad \
	0201.pscad \
	0603.pscad \
	0805.pscad \
	1206.pscad \
	6032.pscad \
	0402.pscad \
	0603p.pscad \
	0805p.pscad \
	1206p.pscad \
	6032p.pscad \
	7343p.pscad \
	CCASE.pscad \
	DCASE.pscad \
	VCASE.pscad \
	qsop-16.pscad \
	R-PDSO-G16.pscad \
	tssop-20.pscad \
	sot23.pscad \
	sot23-6.pscad \
	sot23-gsd.pscad \
	ADE-SMT-8.pscad \
	MLP8.pscad \
	MLP16.pscad \
	S-PVQFN-N64.pscad \
	SolderJumperOpen.pscad \
	SolderJumperClosed.pscad

FP=$(SRC:%.pscad=%.fp)

all: $(FP)

-include $(SRC:%.pscad=.%.d)

%.fp: %.pscad
	@$(PSCAD) -M $*.pscad $*.fp > .$*.d
	@cp -f .$*.d .$*.d.tmp
	@sed -e 's/.*://' -e 's/\\$$//' < .$*.d.tmp | fmt -1 | \
		sed -e 's/^ *//' -e 's/$$/:/' >> .$*.d
	@rm -f .$*.d.tmp
	$(PSCAD) $*.pscad $*.fp

clean:
	-rm -f *.fp .*.d .*.d.tmp
