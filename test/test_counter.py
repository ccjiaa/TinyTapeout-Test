import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_counter_basic(dut):
    """Test basic counting and load functionality."""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset the counter
    dut.rst_n.value = 0
    dut.load.value = 0
    dut.load_value.value = 0
    dut.enable.value = 0
    dut.oe.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Enable counting
    dut.enable.value = 1
    dut.oe.value = 1
    prev_q = 0

    # Count for 10 clock cycles
    for i in range(10):
        await RisingEdge(dut.clk)
        curr_q = dut.q.value.integer
        expected = (prev_q + 1) & 0xFF
        assert curr_q == expected, f"Count mismatch: got {curr_q}, expected {expected}"
        prev_q = curr_q

    # Test synchronous load
    dut.load_value.value = 100
    dut.load.value = 1
    await RisingEdge(dut.clk)
    dut.load.value = 0
    await RisingEdge(dut.clk)

    curr_q = dut.q.value.integer
    assert curr_q == 100, f"Load failed: got {curr_q}, expected 100"
