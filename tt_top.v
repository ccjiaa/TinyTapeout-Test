module tt_top (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        ena,
    input  wire [7:0]  ui_in,
    output wire [7:0]  uo_out
);

    wire [7:0] counter_out;

    counter u_counter (
        .clk(clk),
        .rst_n(rst_n),
        .load(ena),
        .load_value(ui_in),
        .enable(1'b1),
        .oe(1'b1),
        .q(counter_out)
    );

    assign uo_out = counter_out;

endmodule
