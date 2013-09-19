PSCAD=./pscad.py

SRC=\
	dip-32.pscad \
	KK100-3.pscad \
	FTR_SMT-20.pscad \
	45558-0003.pscad \
	pj-012a.pscad \
	pj-202a.pscad \
	cus-14b.pscad \
	jumper5.pscad \
	CP-48-1.pscad \
	DHVQFN14.pscad \
	HEADER_2MM_2x1.pscad \
	HEADER_2MM_2x3.pscad \
	HEADER_2MM_3x6.pscad \
	HEADER_2x1.pscad \
	HEADER_3x1.pscad \
	HEADER_4x1.pscad \
	HEADER_5x1.pscad \
	HEADER_6x1.pscad \
	HEADER_2x5.pscad \
	HEADER_2x6.pscad \
	HEADER_2x7.pscad \
	HEADER_2x16.pscad \
	TE_104118.pscad \
	PowerPAK_SO-8.pscad \
	evqp.pscad \
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
	ddr2_clpr.pscad \
	ddr2_84.pscad \
	7v.pscad \
	FF784.pscad \
	onfi_bga100.pscad \
	PTD08A010W.pscad \
	PTD08A020W.pscad \
	PTD08A0X0W.pscad \
	0201.pscad \
	0603.pscad \
	0805.pscad \
	0806.pscad \
	1206.pscad \
	1411.pscad \
	2312.pscad \
	2917.pscad \
	2924.pscad \
	0402.pscad \
	0402-3.pscad \
	0603p.pscad \
	0805p.pscad \
	0805d.pscad \
	1206p.pscad \
	1411p.pscad \
	2312p.pscad \
	2917p.pscad \
	2924p.pscad \
	BCASE.pscad \
	CCASE.pscad \
	DCASE.pscad \
	VCASE.pscad \
	QSOP-16.pscad \
	DCN-R-PDSO-G8.pscad \
	DGS-S-PDSO-G10.pscad \
	PW-R-PDSO-G16.pscad \
	PW-R-PDSO-G20.pscad \
	DRL-R-PDSO-N5.pscad \
	tssop-20.pscad \
	tssop-24.pscad \
	sot23.pscad \
	sot23-5.pscad \
	sot23-6.pscad \
	sot23-gsd.pscad \
	sot666.pscad \
	ADE-SMT-8.pscad \
	MLP8.pscad \
	MLP16.pscad \
	S-PVQFN-N64.pscad \
	SolderJumperOpen.pscad \
	SolderJumperClosed.pscad \
	MS8E-8.pscad \
	QFN-28.pscad \
	QFN-32.pscad \
	QFN-64.pscad \
	usb-a.pscad \
	usbmini-b.pscad \
	beaglebone.pscad

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
