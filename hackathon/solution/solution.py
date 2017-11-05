"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from hackathon.solution import test

import matplotlib as plt
chargeRate = -1.0
dischargeRate = 2.0

def countNoPower(msg: DataMessage):
    if msg.grid_status == 0:
        test.counter = 0
    else:
        test.counter = test.counter + 1

list =[]

def worker(msg: DataMessage) -> ResultsMessage:
    # breakCounterLs
    countNoPower(msg)
    # racunamo razmak trenutno mesta do zadnje nule

    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    msg.current_load
    # Dummy result is returned in every cycle here
    #osnovna podela da li ima struje ili ne
    load1 = True
    load2 = True
    load3 = True
    power = 0.0
    pv_mode = PVMode.ON

    # if msg.buying_price < 5 and msg.bessSOC < 1 :        #jeftina struja i baterija nije puna -> punimo bateriju
    #     power = chargeRate*1.3
    #
    # if msg.buying_price < 5 and msg.bessSOC < 1 and msg.selling_price < 1\
    #         and msg.solar_production > 2:       #jeftina struja i baterija nije puna i radi solarna -> punimo bateriju vise
    #     power = chargeRate*2

    if msg.current_load < 2.5 and msg.solar_production > msg.current_load:
        power = msg.current_load - msg.solar_production

    if msg.bessSOC > 0.48 and msg.buying_price > 6 and msg.solar_production < msg.current_load:     #baterija puna i struja skupa i nemamo viska od solar prod -> koristimo bateriju
         power = -(msg.solar_production - msg.current_load)

    if msg.bessSOC < 0.3 and msg.grid_status is True:       #ukoliko je baterija jako prazna i ima struje punimo bateriju
        power = chargeRate




    if msg.buying_price > 6 and msg.current_load > 2.5:     #totovo
        load3 = False
    elif msg.current_load > 6 and msg.buying_price < 6:
        load3 = False
    else:
        load3 = True
    #
    # if test.counter >= 1 and test.counter <= 360:              #ako je dugo bilo struje mozes malo vise da prodajes
    #     if(msg.buying_price < 6 and msg.bessSOC < 0.9):
    #         power = chargeRate
    #     elif msg.buying_price > 6 and msg.bessSOC > 0.15 and msg.selling_price > 1:
    #         power = dischargeRate*1.5


    if msg.buying_price > 7:
        if 6.5 <= msg.current_load < 6.7:  # LOAD_2 HIGH_COST BREAKPOINT
            if test.LOAD_2_STATE == 0:  # STATE OFF
                test.LOAD_2_STATE = 1
                test.l2_off_cost = 4
                test.l2_on_cost = 0.4
                load2 = False
        if test.LOAD_2_STATE == 1:  # STATE GAINING
            load2 = False
            test.l2_off_cost += 0.4
            test.l2_on_cost += msg.current_load * 0.5 * 8 / 60
            if abs(test.l2_off_cost - test.l2_on_cost) < 0.5:  # CLOSE ENOUGH
                test.LOAD_2_STATE = 2  # STATE OVERTAKING
        elif test.LOAD_2_STATE == 2:
            load2 = False
            if 6.0 <= msg.current_load < 6.1:
                test.LOAD_2_STATE = 0
                load2 = True



    if msg.grid_status == 0.0 and msg.solar_production < 1.75:
        load2 = False

    if msg.grid_status == 0.0 and msg.solar_production >= 1.75 and msg.solar_production < 4.6:
        load3 = False


    return ResultsMessage(data_msg=msg,
                          load_one=load1,
                          load_two=load2,
                          load_three=load3,
                          power_reference=power,
                          pv_mode=pv_mode)

def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))