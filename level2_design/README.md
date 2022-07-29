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


The clock is assigned using
```
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 
```

```
    # clock
    cocotb.fork(clock_gen(dut.CLK))
```

The reset pulse is assigned using
```
    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
```

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

A ```count``` variable initialized to zero is used to keep track of the no. of sequences detected that is later used to check for the test fail/pass.

The assert statement is used for comparing the ```count``` value to 0 indicating no bugs/ errors in the design.

However,
The following is seen:
```
--ANDN 1                                                     #instruction
VALUE MISMATCH IN DUT = 0x44060109 WITH MODEL = 0x120208a53  #DUT output V/s Model output
--ORN 2
VALUE MATCHES IN DUT = 0x16e27db7f WITH MODEL = 0x16e27db7f
--XNOR 3
VALUE MATCHES IN DUT = 0x4e07512d WITH MODEL = 0x4e07512d
--SLO  4
VALUE MATCHES IN DUT = 0x4268b5bf WITH MODEL = 0x4268b5bf
--SRO  5
VALUE MATCHES IN DUT = 0x1f64268b5 WITH MODEL = 0x1f64268b5
--ROL  6
VALUE MATCHES IN DUT = 0x4268b5b7 WITH MODEL = 0x4268b5b7
--ROR  7
VALUE MATCHES IN DUT = 0x1b64268b5 WITH MODEL = 0x1b64268b5
--SH1ADD  8
VALUE MATCHES IN DUT = 0x19e2b3c3d WITH MODEL = 0x19e2b3c3d
--SH2ADD  9
VALUE MATCHES IN DUT = 0x667852f1 WITH MODEL = 0x667852f1
--SH3ADD  10
VALUE MATCHES IN DUT = 0x1f7128059 WITH MODEL = 0x1f7128059
--SBCLR   11
VALUE MATCHES IN DUT = 0x164268b5b WITH MODEL = 0x164268b5b
--SBSET   12
VALUE MATCHES IN DUT = 0x164268b7b WITH MODEL = 0x164268b7b
--SBINV  13
VALUE MATCHES IN DUT = 0x164268b7b WITH MODEL = 0x164268b7b
--SBEXT  14
VALUE MATCHES IN DUT = 0x1 WITH MODEL = 0x1
--GORC 15 (check)
VALUE MATCHES IN DUT = 0x17666abff WITH MODEL = 0x17666abff
--GREV  16 (should check)
VALUE MATCHES IN DUT = 0x5662a9b5 WITH MODEL = 0x5662a9b5
--SLOI  46
VALUE MATCHES IN DUT = 0xc84d16b7 WITH MODEL = 0xc84d16b7
--SROI 47
VALUE MATCHES IN DUT = 0x1b21345ad WITH MODEL = 0x1b21345ad
--RORI  48
VALUE MATCHES IN DUT = 0x1b21345ad WITH MODEL = 0x1b21345ad
--SBCLRI   49
VALUE MATCHES IN DUT = 0x164268b5b WITH MODEL = 0x164268b5b
--SBSETI   50
VALUE MATCHES IN DUT = 0x164268b5f WITH MODEL = 0x164268b5f
--SBINVI  51
VALUE MATCHES IN DUT = 0x164268b5f WITH MODEL = 0x164268b5f
--SBEXTI  52
VALUE MATCHES IN DUT = 0x1 WITH MODEL = 0x1
--GORCI 57
VALUE MATCHES IN DUT = 0x1e6679fff WITH MODEL = 0x1e6679fff
--GREVI  58
VALUE MATCHES IN DUT = 0xe24714bd WITH MODEL = 0xe24714bd
--CMIX  17
VALUE MATCHES IN DUT = 0x44278939 WITH MODEL = 0x44278939
--CMOV 18
VALUE MATCHES IN DUT = 0x164268b5b WITH MODEL = 0x164268b5b
--FSL 19
VALUE MATCHES IN DUT = 0x4268b5a5 WITH MODEL = 0x4268b5a5
--FSR  20(check)
VALUE MATCHES IN DUT = 0x1964268b5 WITH MODEL = 0x1964268b5
--MIN  35
VALUE MATCHES IN DUT = 0x164268b5b WITH MODEL = 0x164268b5b
--MAX 36
VALUE MATCHES IN DUT = 0xd5de2589 WITH MODEL = 0xd5de2589
--MINU  37
VALUE MATCHES IN DUT = 0xd5de2589 WITH MODEL = 0xd5de2589
--MAXU 38
VALUE MATCHES IN DUT = 0x164268b5b WITH MODEL = 0x164268b5b
--BDEP 39
VALUE MATCHES IN DUT = 0x409a0509 WITH MODEL = 0x409a0509
--BEXT 40
VALUE MATCHES IN DUT = 0xa0cb WITH MODEL = 0xa0cb
--PACK 41
VALUE MATCHES IN DUT = 0x25888b5b WITH MODEL = 0x25888b5b
--PACKU 42
VALUE MATCHES IN DUT = 0xd5df6427 WITH MODEL = 0xd5df6427
--PACKH 45
VALUE MATCHES IN DUT = 0x1895b WITH MODEL = 0x1895b
--SHFL  53
VALUE MATCHES IN DUT = 0x1624694bb WITH MODEL = 0x1624694bb
--UNSHFL  54
VALUE MATCHES IN DUT = 0x1624694bb WITH MODEL = 0x1624694bb
--SHFLI  55 (check)
VALUE MATCHES IN DUT = 0x1a82a4797 WITH MODEL = 0x1a82a4797
--UNSHFLI  56  (check)
VALUE MATCHES IN DUT = 0x1a82a4797 WITH MODEL = 0x1a82a4797

### NUMBER OF BUGS (COUNT) =  1 ###
```

## Test Scenario
    
- Test Inputs: 

    mav_putvalue_src1 = 0xB21345AD
    
    mav_putvalue_src2 = 0x6AEF12C4
    
    mav_putvalue_src3 = 0x223AD49C
    
    mav_putvalue_instr = var_hex[i]
    
- Expected Output: count = 0
- Observed Output in the DUT: count = 1 

Output mismatches for the above inputs proving that there is a design bug

## Design Bug


## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/80892311/180613114-a5a5fac8-9a4d-46a9-b098-9884c0005bf8.png)

The updated design is checked in as mux_fix.v

## Verification Strategy

## Is the verification complete ?

