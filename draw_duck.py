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
	inkwells = dict(red = 'A1', green = 'A2', blue = 'A3', yellow = 'B1', dispense = 'B2')

	wells = dict(
		body = [
			'A4', 'A5', 'A6',
			'B4', 'B6', 
			'C4', 'C5', 'C6',
			'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
			'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 
			'F5', 'F6', 'F7', 'F8'],

		eyes = ['B5'],
		
        feet_and_beak = [
			'C2', 'C3',
            'G6',
            'H5', 'H6'],
	)

	asp_vol = 300.

	def fill(part, color, disp_vol, residual_vol, change):
		for well in wells[part]:
			if residual_vol < disp_vol:
				check_color(change, color, residual_vol)
				residual_vol = asp_vol

			pipette.dispense( disp_vol, canvas[well] )
			residual_vol -= disp_vol
		return residual_vol
			
	def check_color(change, color, residual_vol):
			if change:
				pipette.drop_tip()
				pipette.pick_up_tip()
				pipette.aspirate(asp_vol, palette[inkwells[color]])
			else:
				remaining_ink = asp_vol - residual_vol
				pipette.aspirate(remaining_ink, palette[inkwells[color]])

	def mix(part):
		pipette.dispense(asp_vol, palette[inkwells['dispense']])
		for well in wells[part]:
			pipette.mix(2, 120, canvas[well])
			
	def finish():
		pipette.drop_tip()
		residual_vol = 0.
		return residual_vol

	def main():
		# Yellow ink: Start
		pipette.pick_up_tip()
		residual_vol = 0.

		## Body
		disp_vol = 150.

		pipette.aspirate( asp_vol, palette[inkwells['yellow']] )
		residual_vol = asp_vol

		residual_vol = fill('body','yellow',disp_vol,residual_vol, change=False)

		## Feet and Beak
		disp_vol = 90.

		residual_vol = fill('feet_and_beak','yellow',disp_vol,residual_vol, change=False)

		residual_vol = finish()
		# Yellow ink: End

		# Red ink: Start
		pipette.pick_up_tip()

		pipette.aspirate( asp_vol, palette[inkwells['red']] )
		residual_vol = asp_vol
		## Eyes
		disp_vol = 50.

		residual_vol = fill('eyes','red',disp_vol,residual_vol, change=False)

		## Feet and Beak (Orange)
		disp_vol = 60.

		residual_vol = fill('feet_and_beak','red',disp_vol,residual_vol, change=True)
		mix('feet_and_beak')
		residual_vol = finish()
		# Red ink: End

		# Green ink: Start
		pipette.pick_up_tip()
		eye_asp_vol = 100.
		## Eyes
		disp_vol = 50.

		pipette.aspirate( eye_asp_vol, palette[inkwells['green']] )
		residual_vol = eye_asp_vol

		residual_vol = fill('eyes','green',disp_vol,residual_vol, change=True)

		residual_vol = finish()
		# Green ink: End

		# Blue ink: Start
		pipette.pick_up_tip()
		pipette.aspirate( eye_asp_vol, palette[inkwells['blue']] )
		residual_vol = eye_asp_vol

		residual_vol = fill('eyes','blue',disp_vol,residual_vol, change=True)
		mix('eyes')
		pipette.drop_tip()

	# Main
	main()
