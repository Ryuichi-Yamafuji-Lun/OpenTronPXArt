# -*- coding: utf-8 -*-

from opentrons import protocol_api

metadata = {
	'protocolName': 'Draw Slime',
	'author': 'Ryuichi <ryuichi.y.lun@keio.jp>p>',
	'apiLevel': '2.0'
}

def run(protocol: protocol_api.ProtocolContext):

    # Labware
    tiprack   = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    palette = protocol.load_labware('eppendorf_6_well_cell_culture_plate_5000ul', '2')
    canvas	 = protocol.load_labware('violamo_96_wellplate_370ul', '3')
    pipette   = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

    # Inks prepared in 6-well plate [DISPENSE PLATE HAS TO BE CLEAN]
    inkwells = dict(red = 'A1', green = 'A2', blue = 'A3', yellow = 'B1', dispense = 'B2')

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
    )

    asp_vol = 300.
    withdraw_vol = 75.

    def fill(part, color, disp_vol):
        pipette.pick_up_tip()
        pipette.aspirate( asp_vol, palette[inkwells[color]])
        residual_vol = asp_vol
        for well in wells[part]:
            if residual_vol < disp_vol:
                pipette.drop_tip()
                pipette.pick_up_tip()
                pipette.aspirate(asp_vol, palette[inkwells[color]])
                residual_vol = asp_vol

            pipette.dispense( disp_vol, canvas[well] )
            residual_vol -= disp_vol
            
    def mix(part):
        pipette.dispense(asp_vol, palette[inkwells['dispense']])
        for well in wells[part]:
            pipette.mix(2, 120, canvas[well])
        pipette.drop_tip()

    # Initial withdraw from the slime to change color
    def withdraw(part, withdraw_vol):
        pipette.pick_up_tip()
        ## Begin withdrawal
        pipette_vol = 0.
        for well in wells[part]:
            ## If pipette tip is full dispense
            if pipette_vol == asp_vol:
                pipette.dispense( asp_vol, palette[inkwells['dispense']] )
                pipette_vol = 0.
            pipette.aspirate( withdraw_vol, canvas[well] )
            pipette_vol += withdraw_vol
        ## Finish withdrawal
        pipette.drop_tip()
            

    def main():
        # Ink volume total has to be 75
        red = 23.
        green = 6.
        blue = 9.
        yellow = 37.

        # Withdraw ink: Start
        withdraw('body', withdraw_vol)

        # Red ink: Start
        fill('body','red', red)
        pipette.drop_tip()

        # Green ink: Start
        fill('body','green', green)
        pipette.drop_tip()

        # Blue ink: Start
        fill('body','blue', blue)
        pipette.drop_tip()

        # Yellow ink: Start
        fill('body','yellow', yellow)

        # Mix 
        mix('body')
    
    main()


        

