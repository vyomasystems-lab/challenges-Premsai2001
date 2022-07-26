# 31:1 MUX Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod ID is included in the screenshot below:*

![image](https://user-images.githubusercontent.com/80892311/180588458-c4ca3d30-ad7f-4960-8820-4af728d34090.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 31  2-bit inputs *in0* - *in30* and based on the value in the select line *sel*, which gives a 2-bit output *out*.

Input values are generated at random as shown:
```
#generate random inputs
    in_val = []
    for i in range(31):
        x = random.randint(0,3)
        in_val.append(x)
```

The select line value is generated as shown:
```
for j in range(31):
        select = j
```

These input values are assigned to the input ports using 
```
    dut.inp0.value = in_val[0]
    dut.inp1.value = in_val[1]
    .
    .
    .
    dut.inp29.value = in_val[29]
    dut.inp30.value = in_val[30]
    dut.sel.value = select
```
A ```count``` variable initialized to zero is used to keep track of the no. of sequences detected that is later used to check for the test fail/pass.
The assert statement is used for comparing the ```count``` value to 0 indicating no bugs/ errors in the design.

The following errors are seen:
```
[0, 2, 1, 1, 0, 2, 3, 3, 2, 0, 3, 3, 1, 1, 3, 0, 1, 1, 1, 3, 1, 0, 0, 0, 3, 1, 3, 3, 1, 3, 3]
    28.00ns INFO     ERROR: MUX result is incorrect: For select = 12 , out = 0, but expected value = 1
    62.00ns INFO     ERROR: MUX result is incorrect: For select = 30 , out = 0, but expected value = 3
    62.00ns INFO     test_mux failed
```
```              
    assert count == 0, f'MUX DESIGN contains {count} BUG/BUGS INDICATED BY THE ABOVE STATEMENTS'
    AssertionError: MUX DESIGN contains 2 BUG/BUGS INDICATED BY THE ABOVE STATEMENTS
```                     

## Test Scenario
- Test Inputs: in_val = [0, 2, 1, 1, 0, 2, 3, 3, 2, 0, 3, 3, 0, 1, 3, 0, 1, 1, 1, 3, 1, 0, 0, 0, 3, 1, 3, 3, 1, 3, 3]; select = 12
- Expected Output: out = 1
- Observed Output in the DUT dut.out=0

- Test Inputs: in_val = [0, 2, 1, 1, 0, 2, 3, 3, 2, 0, 3, 3, 0, 1, 3, 0, 1, 1, 1, 3, 1, 0, 0, 0, 3, 1, 3, 3, 1, 3, 3]; select = 30
- Expected Output: out = 3
- Observed Output in the DUT dut.out=0

Output mismatches for the above inputs proving that there is a design bug.

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
      5'b01101: out = inp12; ===> BUG: invalid assignment
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

## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/80892311/180613114-a5a5fac8-9a4d-46a9-b098-9884c0005bf8.png)

The updated design is checked in as mux_fix.v
