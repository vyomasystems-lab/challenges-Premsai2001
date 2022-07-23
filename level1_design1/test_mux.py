# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    cocotb.log.info('##### CTB: Develop your test here ########')
    in_val = [1,2,3,0,0,1,2,2,0,3,1,2,3,1,1,2,3,0,1,0,3,2,0,1,0,2,0,1,1,2,3]
    select = 12

    # input driving
    dut.inp0.value = in_val[0]
    dut.inp1.value = in_val[1]
    dut.inp2.value = in_val[2]
    dut.inp3.value = in_val[3]
    dut.inp4.value = in_val[4]
    dut.inp5.value = in_val[5]
    dut.inp6.value = in_val[6]
    dut.inp7.value = in_val[7]
    dut.inp8.value = in_val[8]
    dut.inp9.value = in_val[9]
    dut.inp10.value = in_val[10]
    dut.inp11.value = in_val[11]
    dut.inp12.value = in_val[12]
    dut.inp13.value = in_val[13]
    dut.inp14.value = in_val[14]
    dut.inp15.value = in_val[15]
    dut.inp16.value = in_val[16]
    dut.inp17.value = in_val[17]
    dut.inp18.value = in_val[18]
    dut.inp19.value = in_val[19]
    dut.inp20.value = in_val[20]
    dut.inp21.value = in_val[21]
    dut.inp22.value = in_val[22]
    dut.inp23.value = in_val[23]
    dut.inp24.value = in_val[24]
    dut.inp25.value = in_val[25]
    dut.inp26.value = in_val[26]
    dut.inp27.value = in_val[27]
    dut.inp28.value = in_val[28]
    dut.inp29.value = in_val[29]
    dut.inp30.value = in_val[30]
    dut.sel.value = select

    await Timer(2, units='ns')
    
    for i in range(31):
     if select==i :
        assert dut.out.value == in_val[i], "MUX result is incorrect: For sel = {i} , out = {OUT}, but expected value = {exp}".format(
             i = int(i), OUT=int(dut.out.value), exp = int(in_val[i]))
   
@cocotb.test()
async def randomized_test_mux(dut):
    for j in range(5):
        in_val = []
        for i in range(31):
            x = random.randint(0,3)
            in_val.append(x)
        print(in_val)
        select = random.randint(0,30)
        print(select)

        dut.inp0.value = in_val[0]
        dut.inp1.value = in_val[1]
        dut.inp2.value = in_val[2]
        dut.inp3.value = in_val[3]
        dut.inp4.value = in_val[4]
        dut.inp5.value = in_val[5]
        dut.inp6.value = in_val[6]
        dut.inp7.value = in_val[7]
        dut.inp8.value = in_val[8]
        dut.inp9.value = in_val[9]
        dut.inp10.value = in_val[10]
        dut.inp11.value = in_val[11]
        dut.inp12.value = in_val[12]
        dut.inp13.value = in_val[13]
        dut.inp14.value = in_val[14]
        dut.inp15.value = in_val[15]
        dut.inp16.value = in_val[16]
        dut.inp17.value = in_val[17]
        dut.inp18.value = in_val[18]
        dut.inp19.value = in_val[19]
        dut.inp20.value = in_val[20]
        dut.inp21.value = in_val[21]
        dut.inp22.value = in_val[22]
        dut.inp23.value = in_val[23]
        dut.inp24.value = in_val[24]
        dut.inp25.value = in_val[25]
        dut.inp26.value = in_val[26]
        dut.inp27.value = in_val[27]
        dut.inp28.value = in_val[28]
        dut.inp29.value = in_val[29]
        dut.inp30.value = in_val[30]
        dut.sel.value = select

        await Timer(2, units='ns')
        
       # dut._log.info(f'A={A:05} B={B:05} model={A+B:05} DUT={int(dut.sum.value):05}')
        for i in range(31):
            if select==i :
             assert dut.out.value == in_val[i], "MUX result is incorrect: For sel = {i} , out = {OUT}, but expected value = {exp}".format(
                 i = int(i), OUT=int(dut.out.value), exp = int(in_val[i]))