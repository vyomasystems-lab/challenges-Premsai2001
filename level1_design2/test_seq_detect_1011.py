# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await Timer(10, units='ns')
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')
    var = [0,1,0,1,0,1,1,0,1,1]
    count = 0
    for i in range(len(var)):
        dut.inp_bit.value = var[i]
        await FallingEdge(dut.clk)
        if(dut.seq_seen.value==1): count= count +1
        #dut._log.info(f"curr_state = {dut.current_state.value}")
        #dut._log.info(f"next_state = {dut.next_state.value}")
    assert count>0, f"output not detected"
    print(count)
    
