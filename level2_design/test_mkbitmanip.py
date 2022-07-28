# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    count= 0 
    var_inst = ['ANDN','ORN']#'XNORN','SLO','SRO','ROL','ROR','SBCLR','SBSET','SBINV','SBEXT']
    var_hex = [0x401070B3, 0x401060B3]
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x0
    mav_putvalue_src3 = 0x0
    for i in range(2):
        mav_putvalue_instr = var_hex[i]

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
        
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
            
        error_message = f'VALUE MISMATCH IN DUT = {hex(dut_output)} WITH MODEL = {hex(expected_mav_putvalue)}'
        pass_message = f'VALUE MATCHES IN DUT = {hex(dut_output)} WITH MODEL = {hex(expected_mav_putvalue)}'
        # comparison
        if(dut_output != expected_mav_putvalue):
            count = count + 1
            print(error_message)
        elif(dut_output == expected_mav_putvalue):
            print(pass_message)

    assert count == 0, f'FEW INSTRUCTIONS ARE BUGGY'