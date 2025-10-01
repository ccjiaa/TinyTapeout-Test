import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_counter(dut):
    # Start clock with 10ns period
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Initially enable = 0, load = 0
    dut.ui.value = 0

    # Wait a few cycles
    for _ in range(3):
        await RisingEdge(dut.clk)

    # Load a value: ui[1] = load = 1, ui[7:0] = 123
    load_val = 123
    dut.ui.value = (1 << 1) | load_val  # load bit + load value bits
    await RisingEdge(dut.clk)

    # Load bit low again
    dut.ui.value = 0
    await RisingEdge(dut.clk)

    # Check output uo matches loaded value
    assert dut.uo.value.integer == load_val, f"Expected uo={load_val}, got {dut.uo.value.integer}"

    # Enable counting: ui[0] = enable = 1, ui[1] = load = 0
    dut.ui.value = 1
    await RisingEdge(dut.clk)

    # Check uo incremented by 1
    expected = load_val + 1
    assert dut.uo.value.integer == expected, f"Expected uo={expected}, got {dut.uo.value.integer}"

    # Wait a few cycles with enable on, check counting
    for i in range(2, 5):
        await RisingEdge(dut.clk)
        expected = load_val + i
        assert dut.uo.value.integer == expected, f"Expected uo={expected}, got {dut.uo.value.integer}"

