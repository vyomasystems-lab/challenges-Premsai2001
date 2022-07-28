# BIT-MANIPULATION COPROCESSOR Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod ID is included in the screenshot below:*

![image](https://user-images.githubusercontent.com/80892311/181633067-40f8225a-8cf4-4957-b849-c2e3d41738c4.png)


## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (``mkbitmanip`` module here) which 
takes 4 inputs
- mav_putvalue_instr -> 32 bit
- mav_putvalue_src1  -> 32 bit
- mav_putvalue_src2  -> 32 bit
- mav_putvalue_src3  -> 32 bit

and 1 output
- mav_putvalue -> 33 bit


The values are assigned to the input ports as an array using 
```
    var_hex = [0x401070B3, 0x401060B3, 0x401040B3, 0x201010B3, 0x201050B3, 0x601010B3, 0x601050B3, 0x201020B3, 0x201040B3, 
    0x201060B3, 0x481010B3, 0x281010B3, 0x681010B3,0x481050B3, 0x281050B3, 0x681050B3, 0x20101093, 0x20105093, 0x60105093, 
    0x48101093, 0x28101093, 0x68101093, 0x48105093, 0x28105093, 0x68105093, 0x061010B3, 0x061050B3, 0x041010B3, 0x041050B3,
    0x0A1040B3, 0x0A1050B3, 0x0A1060B3, 0x0A1070B3, 0x481060B3, 0x081060B3, 0x081040B3, 0x481040B3, 0x081070B3,
    0x081010B3, 0x081050B3, 0x08101093, 0x08105093]
    
    mav_putvalue_src1 = 0xB21345AD
    mav_putvalue_src2 = 0x6AEF12C4
    mav_putvalue_src3 = 0x223AD49C
    
    for i in range(42):
        mav_putvalue_instr = var_hex[i]

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
```

The assert statement is used for comparing the multiplexer's outut to the expected value.

The following errors are seen:
```
assert dut.out.value == in_val[i], "MUX result is incorrect: For sel = {i} , out = {OUT}, but expected value = {exp}".format(
                     AssertionError: MUX result is incorrect: For sel = 12 , out = 0, but expected value = 3
```
```
 assert dut.out.value == in_val[i], "MUX result is incorrect: For sel = {i} , out = {OUT}, but expected value = {exp}".format(
                     AssertionError: MUX result is incorrect: For sel = 30 , out = 0, but expected value = 2
```
## Test Scenario
- Test Inputs: in_val = [1, 2, 3, 0, 0, 1, 2, 2, 0, 3, 1, 2, 3, 1, 1, 2, 3, 0, 1, 0, 3, 2, 0, 1, 0, 2, 0, 1, 1, 2, 2]; select = 12
- Expected Output: out = 3
- Observed Output in the DUT dut.out=0

- Test Inputs: in_val = [1, 2, 3, 0, 0, 1, 2, 2, 0, 3, 1, 2, 3, 1, 1, 2, 3, 0, 1, 0, 3, 2, 0, 1, 0, 2, 0, 1, 1, 2, 2]; select = 30
- Expected Output: out = 2
- Observed Output in the DUT dut.out=0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
always @(sel or inp0  or inp1 or  inp2 or inp3 or inp4 or inp5 or inp6 or
            inp7 or inp8 or inp9 or inp10 or inp11 or inp12 or inp13 or 
            inp14 or inp15 or inp16 or inp17 or inp18 or inp19 or inp20 or
            inp21 or inp22 or inp23 or inp24 or inp25 or inp26 or inp27 or 
            inp28 or inp29 or inp30 )

  begin
    case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12; ===> BUG
      5'b01101: out = inp13;
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;
      ======================> BUG: missing CASE
      default: out = 0;
    endcase
  end
```
For the MUX design, 
- the case statement for ``sel = 12`` should be ``5'b01100: out = inp12`` instead of ``5'b01101: out = inp12`` in the design code.
- the case statement for ``sel = 30`` i.e ``5'b11110: out = inp30`` is missing in the design code.
- 
## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/80892311/180613114-a5a5fac8-9a4d-46a9-b098-9884c0005bf8.png)

The updated design is checked in as mux_fix.v

## Verification Strategy

## Is the verification complete ?

