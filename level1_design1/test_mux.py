# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    cocotb.log.info('##### CTB: Develop your test here ########')
    in0 = 0
    in1 = 1
    in2 = 2
    in3 = 3
    in4 = 3
    in5 = 2
    in6 = 1
    in7 = 2
    in8 = 3
    in9 = 1
    in10 = 0
    in11 = 1
    in12 = 2
    in13 = 3
    in14 = 3
    in15 = 2
    in16 = 1
    in17 = 2
    in18 = 3
    in19 = 1
    in20 = 0
    in21 = 1
    in22 = 2
    in23 = 3
    in24 = 3
    in25 = 2
    in26 = 1
    in27 = 2
    in28 = 3
    in29 = 1
    in30 = 0
    select = 12

    # input driving
    dut.inp0.value = in0
    dut.inp1.value = in1
    dut.inp2.value = in2
    dut.inp3.value = in3
    dut.inp4.value = in4
    dut.inp5.value = in5
    dut.inp6.value = in6
    dut.inp7.value = in7
    dut.inp8.value = in8
    dut.inp9.value = in9
    dut.inp10.value = in10
    dut.inp11.value = in11
    dut.inp12.value = in12
    dut.inp13.value = in13
    dut.inp14.value = in14
    dut.inp15.value = in15
    dut.inp16.value = in16
    dut.inp17.value = in17
    dut.inp18.value = in18
    dut.inp19.value = in19
    dut.inp20.value = in20
    dut.inp21.value = in21
    dut.inp22.value = in22
    dut.inp23.value = in23
    dut.inp24.value = in24
    dut.inp25.value = in25
    dut.inp26.value = in26
    dut.inp27.value = in27
    dut.inp28.value = in28
    dut.inp29.value = in29
    dut.inp30.value = in30
    dut.sel.value = select

    await Timer(2, units='ns')
    
    assert dut.out.value == A+B, "Adder result is incorrect: {A} + {B} != {SUM}, expected value={EXP}".format(
            A=int(dut.a.value), B=int(dut.b.value), SUM=int(dut.sum.value), EXP=A+B)