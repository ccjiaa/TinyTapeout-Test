import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_counter(dut):
    """Test the 8-bit counter using ui bits directly"""

    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz clock
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.ui.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # Wait a few cycles for reset to propagate
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Load value 123 into counter:
    load_val = 123
    # Set ui: bit 1 = load, bits [7:0] = load_value
    dut.ui.value = (load_val & 0xFF) | (1 << 1)  # load=1
    await RisingEdge(dut.clk)
    # Clear load
    dut.ui.value = 0
    await RisingEdge(dut.clk)

    assert dut.uo.value.integer == load_val, f"Load failed: expected {load_val}, got {dut.uo.value.integer}"

    # Enable counting:
    dut.ui.value = 1  # enable=1, load=0
    await RisingEdge(dut.clk)
    expected = (load_val + 1) & 0xFF
    assert dut.uo.value.integer == expected, f"Count failed: expected {expected}, got {dut.uo.value.integer}"

    # Advance a few counts
    for i in range(2, 5):
        await RisingEdge(dut.clk)
        expected = (load_val + i) & 0xFF
        assert dut.uo.value.integer == expected, f"Count failed at step {i}: expected {expected}, got {dut.uo.value.integer}"
