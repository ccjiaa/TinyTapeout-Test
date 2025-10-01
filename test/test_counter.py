import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def test_counter(dut):
    """Test programmable 8-bit counter"""

    # Start a clock with 10ns period
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.load.value = 0
    dut.enable.value = 0
    dut.oe.value = 1
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Wait for a few cycles
    for _ in range(2):
        await RisingEdge(dut.clk)

    # Load value synchronously
    dut.load_value.value = 123
    dut.load.value = 1
    await RisingEdge(dut.clk)
    dut.load.value = 0

    assert dut.q.value == 123, f"Expected 123 after load, got {dut.q.value}"

    # Enable counting
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    assert dut.q.value == 124, f"Expected 124 after count, got {dut.q.value}"

    # Check tri-state behavior
    dut.oe.value = 0
    await Timer(1, units="ns")
    assert dut.q.value.is_resolvable == False, "Output should be high-impedance when oe=0"
