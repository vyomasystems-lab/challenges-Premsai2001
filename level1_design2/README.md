# Sequence Detector 1011 (Overlapping) Design Verification
The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*The Gitpod ID is included in the screenshot below:*

![image](https://user-images.githubusercontent.com/80892311/180844462-25b5d4f2-f9dd-4d22-87f3-9e35b40f1f56.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 31  2-bit inputs *in0* - *in30* and based on the value in the select line *sel*, which gives a 2-bit output *out*.

The clock is assigned using
```
clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
cocotb.start_soon(clock.start())        # Start the clock
```

The reset pulse is assigned using
```
dut.reset.value = 1
await FallingEdge(dut.clk)  
dut.reset.value = 0
await FallingEdge(dut.clk)
 ```
 
The values are assigned to the input ports as an array using 
```
var = [1,0,1,0,1,1,0]
for i in range(7):
    in_bit = var[i]
    print(in_bit)
    dut.inp_bit.value = in_bit
```

The assert statement is used for comparing the multiplexer's outut to the expected value.
```
assert dut.seq_seen.value == 1, " Sequnece is present but not detected "
```

The following error is seen:
```
 assert dut.seq_seen.value == 1, " Sequence is present but not detected "
                     AssertionError:  Sequence is present but not detected
```

## Test Scenario
- Test Inputs: var = [1,0,1,0,1,1,0]
- Expected Output: seq_seen = 1
- Observed Output in the DUT dut.seq_seen = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following
```
case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE; 
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;       ===> BUG
      end
      SEQ_1011:
      begin
        next_state = IDLE;         ===> BUG
      end
    endcase
  end
```
For the 1011 Sequence detector design,
- due to the state transition to IDLE during ``inp_bit=0` for both the cases of ``SEQ_101`` and ``SEQ_011``, the overlapping sequence detection doesn't occur.

## Design Fix
Updating the design and re-running the test makes the test pass.

The updated design is checked in as seq_detect_1011_fix.v