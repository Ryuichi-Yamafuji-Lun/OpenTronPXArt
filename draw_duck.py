#Create DUCK pixel art

from opentrons import protocol_api

metadata = {
	'protocolName': 'Draw Duck',
	'author': 'Lianne <knsktzkml@gmail.com>, Katelyn <ynaito@sfc.keio.ac.jp>, Ryuichi <ryuichi.y.lun@keio.jp>',
	'apiLevel': '2.0'
}

def run(protocol: protocol_api.ProtocolContext):

	# Labware
	tiprack   = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
	palette = protocol.load_labware('eppendorf_6_well_cell_culture_plate_5000ul', '2')
	canvas	 = protocol.load_labware('violamo_96_wellplate_370ul', '3')
	pipette   = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

	# Inks prepared in 6-well plate
	inkwells = dict(red = 'A1', green = 'A2', blue = 'A3', yellow = 'B1', orange = 'B2')

	wells = dict(
		body = [
			'A4', 'A5', 'A6',
			'B4', 'B6', 
			'C4', 'C5', 'C6',
			'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
			'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 
			'F5', 'F6', 'F7', 'F8'],

		beak = ['C2', 'C3'],

		eyes = ['B5'],
		
        feet = [
            'G6',
            'H5', 'H6'],
	)

	asp_vol = 300.

	def fill(part, color, disp_vol,residual_vol):
		for well in wells[part]:
			if residual_vol < disp_vol:
				pipette.aspirate( asp_vol - residual_vol, palette[inkwells[color]] )
				residual_vol = asp_vol

			pipette.dispense( disp_vol, canvas[well] )
			residual_vol -= disp_vol

	# Yellow ink
	def yellow_ink():
		## Start
		pipette.pick_up_tip()
		residual_vol = 0.
		## Body
		disp_vol = 150.
		pipette.aspirate( asp_vol, palette[inkwells['yellow']] )
		residual_vol = asp_vol
		fill('body', 'yellow', disp_vol, residual_vol)
		return residual_vol

    # Orange ink
	def orange_ink(residual_vol):
		## Start
		yellow_ink_total = 360. - residual_vol
		## Create Orange
		### Yellow
		pipette.dispense( residual_vol, palette[inkwells['orange']])
		residual_vol = 0.
		yellow_asp_vol = 70.
		while yellow_ink_total > 0:
			pipette.aspirate( yellow_asp_vol, palette[inkwells['yellow']] )
			pipette.dispense( yellow_asp_vol, palette[inkwells['orange']] )
			yellow_ink_total -= yellow_asp_vol

		pipette.drop_tip()

		### Red
		red_ink_total = 540.
		red_asp_vol = 180.
		pipette.pick_up_tip()
		while red_ink_total > 0:
			pipette.aspirate( red_asp_vol, palette[inkwells['red']] )
			pipette.dispense( red_asp_vol, palette[inkwells['orange']] )
			red_ink_total -= red_asp_vol

		## Eye: red
		disp_vol = 50
		fill('eyes', 'red', disp_vol, residual_vol)

		## Mix Master
		pipette.mix( 4, 150, palette[inkwells['orange']])

		## Beak
		disp_vol = 150.
		pipette.aspirate( asp_vol, palette[inkwells['orange']] )
		residual_vol = asp_vol
		fill('beak', 'orange', disp_vol, residual_vol)

		## Feet
		pipette.aspirate( asp_vol, palette[inkwells['orange']] )
		residual_vol = asp_vol
		fill('feet', 'orange', disp_vol, residual_vol)
		
		# End
		pipette.drop_tip()

    # Black ink
	def black_ink():
		## Start
		pipette.pick_up_tip()
		residual_vol = 0.
		asp_vol = 50
		## Eye
		disp_vol = 50.
		## Green
		pipette.aspirate( asp_vol, palette[inkwells['green']] )
		residual_vol = asp_vol
		fill('eyes', 'green', disp_vol, residual_vol)
		pipette.drop_tip()
		
		## Blue
		pipette.pick_up_tip()
		residual_vol = 0.
		pipette.aspirate( asp_vol, palette[inkwells['blue']] )
		residual_vol = asp_vol
		fill('eyes', 'blue', disp_vol, residual_vol)

		## Mix
		for well in wells['eyes']:
			pipette.mix(2, 120, canvas[well])

		## End
		pipette.drop_tip()
	
	# Main
	residual_vol = yellow_ink()
	orange_ink(residual_vol)
	black_ink()
	