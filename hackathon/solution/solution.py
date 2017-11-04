"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from hackathon.solution import test

chargeRate = -1.0
dischargeRate = 2.0

list=[]

def countNoPower(msg: DataMessage):
    if msg.grid_status == 0:
        test.counter = 0
    else:
        test.counter = test.counter + 1

def worker(msg: DataMessage) -> ResultsMessage:
    # breakCounterLs
    countNoPower(msg)
    # racunamo razmak trenutno mesta do zadnje nule

    list.append(1)

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

    if msg.buying_price < 5 and msg.bessSOC < 1:        #jeftina struja i baterija nije puna -> punimo bateriju
        power = chargeRate*0.79
    if msg.buying_price < 5 and msg.bessSOC < 1 and msg.selling_price < 1 and msg.solar_production > 2:        #jeftina struja i baterija nije puna -> punimo bateriju
        power = chargeRate*6

    if msg.bessSOC > 0.63 and msg.buying_price > 6:          #baterija puna i struja skupa -> koristimo bateriju
        power = dischargeRate                               #TODO pokriti slucaj kada je prekid bio u zadnjih 8 sati

    if msg.bessSOC < 0.3 and msg.grid_status is True:       #ukoliko je baterija jako prazna i ima struje punimo bateriju
        power = chargeRate

    if msg.grid_status is False and msg.bessSOC > 0.05:     #ukoliko nestane struje koristi se baterija
        power = 6.0

    if msg.buying_price > 6 and msg.current_load > 2.5:     #totovo
        load3 = False
    elif msg.current_load > 6 and msg.buying_price < 6:
        load3 = False
    else:
        load3 = True

    if test.counter >= 1 and test.counter <= 400:              #ako je dugo bilo struje mozes malo vise da prodajes
        if(msg.buying_price < 6 and msg.bessSOC < 0.9):
            power = chargeRate
        elif msg.buying_price > 6 and msg.bessSOC > 0.15 and msg.selling_price > 1:
            power = dischargeRate*1.5
    #kupujemo po jeftinoj
    if msg.buying_price < 5 and msg.mainGridPower > 0 :
        test.sumCheap += msg.mainGridPower * msg.buying_price / 60;
    # kupujemo po skupoj
    if msg.buying_price > 5 and msg.mainGridPower > 0:
        test.sumExp += msg.mainGridPower * msg.buying_price / 60;

    if msg.mainGridPower < 0 and msg.selling_price < 1:
        test.sumSoldCheap += msg.mainGridPower * msg.selling_price / 60

    if msg.mainGridPower < 0 and msg.selling_price > 1:
        test.sumSoldExp += msg.mainGridPower * msg.selling_price / 60


    if len(list) == 1439:
        f = open('helloworld.txt', 'w')
        f.write("\nSum Exp: " + str(test.sumExp) +" \nSum Cheap: " + str(test.sumCheap) + "\n sumSoldCheap: " + str(test.sumSoldCheap) + "\n sumSoldExp: " + str(test.sumSoldExp))
        f.write(" \nZbir: " + str(test.sumCheap + test.sumExp + test.sumSoldExp))
        f.close()


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