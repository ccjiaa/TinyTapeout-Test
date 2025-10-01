`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb();

  reg clk = 0;
  reg rst_n = 0;
  reg [7:0] ui_in = 0;
  wire [7:0] uo_out;
  wire [7:0] uio_in;

  // Instantiate your module with matching ports
  tt_um_ccjiaa_counter user_project (
      .clk(clk),
      .rst_n(rst_n),
      .ui(ui_in),
      .uo(uo_out),
      .uio(uio_in)
  );

  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);

    // Initialize signals
    rst_n = 0;
    #20;
    rst_n = 1;

    ui_in = 8'h01; // example input

    // Clock generation
    forever #5 clk = ~clk;
  end

endmodule
