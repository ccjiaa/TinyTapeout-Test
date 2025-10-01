import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_counter(dut):
    """Test the 8-bit counter using ui bus for control signals."""

    # Start clock with 10 ns period
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut.rst_n.value = 0
    dut.ui.value = 0  # clear inputs
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # Load a value into the counter:
    # ui[1] = load = 1
    # ui[7:0] = load_value = 123 (0x7B)
    load_value = 123
    dut.ui.value = (1 << 1) | load_value
    await RisingEdge(dut.clk)

    # Remove load signal (ui[1]) to zero so counter can run
    dut.ui.value = 0
    await RisingEdge(dut.clk)

    # Check if the counter loaded correctly
    assert dut.uo.value == load_value, f"Expected counter load {load_value}, got {dut.uo.value}"

    # Enable counting: ui[0] = enable = 1
    dut.ui.value = 1
    await RisingEdge(dut.clk)

    # Counter should increment by 1
    expected = (load_value + 1) & 0xFF
    assert dut.uo.value == expected, f"Expected counter increment {expected}, got {dut.uo.value}"

    # Let counter count a few more cycles
    for i in range(5):
        await RisingEdge(dut.clk)
        expected = (expected + 1) & 0xFF
        assert dut.uo.value == expected, f"At cycle {i+1}, expected {expected}, got {dut.uo.value}"

    # Reset again and check counter resets to zero
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    assert dut.uo.value == 0, f"Expected counter reset to 0, got {dut.uo.value}"
