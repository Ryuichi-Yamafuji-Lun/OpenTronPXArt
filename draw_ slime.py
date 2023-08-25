# -*- coding: utf-8 -*-

from opentrons import protocol_api

metadata = {
	'protocolName': 'Draw Slime',
	'author': 'Kensuke Tozuka <knsktzkml@gmail.com>, Yasuhiro Naito <ynaito@sfc.keio.ac.jp>',
	'apiLevel': '2.0'
}

def run(protocol: protocol_api.ProtocolContext):

	# Labware
	tiprack   = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
	palette = protocol.load_labware('eppendorf_6_well_cell_culture_plate_5000ul', '2')
	canvas	 = protocol.load_labware('violamo_96_wellplate_370ul', '3')
	pipette   = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

	# Inks prepared in 6-well plate
	inkwells = dict(red = 'A1', green = 'A2', blue = 'A3')

	wells = dict(

		body = [
			'A6', 'A7',
			'B5', 'B6', 'B7', 'B8',
			'C4', 'C6', 'C7', 'C9',
			'D3', 'D10',
			'E2', 'E3', 'E4', 'E6', 'E7', 'E9', 'E10', 'E11',
			'F2', 'F3', 'F5', 'F6', 'F7', 'F8', 'F10', 'F11',
			'G3', 'G4', 'G9', 'G10',
			'H4', 'H5', 'H6', 'H7', 'H8', 'H9' ],

		mouth = [
			'F4', 'F9',
			'G5', 'G6', 'G7', 'G8' ],

		eyes = ['D5', 'D8'],
	)


	asp_vol = 300.

	# Blue ink: Start
	pipette.pick_up_tip()
	residual_vol = 0.

	## Body
	disp_vol = 50.

	pipette.aspirate( asp_vol, palette[inkwells['blue']] )
	residual_vol = asp_vol

	for well in wells['body']:
		if residual_vol < disp_vol:
			pipette.aspirate( asp_vol - residual_vol, palette[inkwells['blue']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	## Eyes
	disp_vol = 50.

	for well in wells['eyes']:
		if residual_vol < disp_vol:
			pipette.aspirate( asp_vol - residual_vol, palette[inkwells['blue']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	pipette.drop_tip()
	# Blue ink: End

	# Red ink: Start
	pipette.pick_up_tip()
	residual_vol = 0.

	## Mouth
	disp_vol = 150.

	pipette.aspirate( asp_vol, palette[inkwells['red']] )
	residual_vol = asp_vol

	for well in wells['mouth']:
		if residual_vol < disp_vol:
			pipette.aspirate( asp_vol - residual_vol, palette[inkwells['red']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	## Eyes
	disp_vol = 50.

	for well in wells['eyes']:
		if residual_vol < disp_vol:
			pipette.drop_tip()
			pipette.pick_up_tip()
			pipette.aspirate( asp_vol, palette[inkwells['red']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	## Body
	disp_vol = 100.

	for well in wells['body']:
		if residual_vol < disp_vol:
			pipette.drop_tip()
			pipette.pick_up_tip()
			pipette.aspirate( asp_vol, palette[inkwells['red']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	pipette.drop_tip()
	# Red ink: End

	# Green ink: Start
	pipette.pick_up_tip()
	residual_vol = 0.

	## Eyes
	disp_vol = 50.

	pipette.aspirate( asp_vol, palette[inkwells['green']] )
	residual_vol = asp_vol

	for well in wells['eyes']:
		if residual_vol < disp_vol:
			pipette.drop_tip()
			pipette.pick_up_tip()
			pipette.aspirate( asp_vol, palette[inkwells['green']] )
			residual_vol = asp_vol

		pipette.dispense( disp_vol, canvas[well] )
		residual_vol -= disp_vol

	pipette.drop_tip()
	# Green ink: End

	# Mix
	## Body
	pipette.pick_up_tip()
	for well in wells['body']:
		pipette.mix(2, 120, canvas[well])
	pipette.drop_tip()

	## Eyes
	pipette.pick_up_tip()
	for well in wells['eyes']:
		pipette.mix(2, 120, canvas[well])
	pipette.drop_tip()
