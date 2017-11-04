"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from hackathon.solution import test

chargeRate = -1.0
dischargeRate = 2.0

def countNoPower(msg: DataMessage):
    if msg.grid_status == 0:
        test.counter = 0
    else:
        test.counter = test.counter + 1

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

    if msg.buying_price < 5 and msg.bessSOC < 0.95:        #jeftina struja i baterija nije puna -> punimo bateriju
        power = chargeRate

    if msg.bessSOC > 0.8 and msg.buying_price > 6:          #baterija puna i struja skupa -> koristimo bateriju
        power = dischargeRate                               #TODO pokriti slucaj kada je prekid bio u zadnjih 8 sati

    if msg.bessSOC < 0.3 and msg.grid_status is True:       #ukoliko je baterija jako prazna i ima struje punimo bateriju
        power = chargeRate

    if msg.grid_status is False and msg.bessSOC > 0.05:     #ukoliko nestane struje koristi se baterija
        power = 6.0

    if msg.buying_price > 6 and msg.current_load > 2.5:
        load3 = False
    elif msg.current_load > 6 and msg.buying_price < 6:
        load3 = False
    else:
        load3 = True

    if(test.counter >= 1 and test.counter <= 360):
        if(msg.buying_price < 6 and msg.bessSOC < 0.9):
            power = chargeRate
        elif msg.buying_price > 6 and msg.bessSOC > 0.15 and msg.selling_price > 1:
            power = dischargeRate*1.5

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