module tt_um_ccjiaa_counter (
    input  wire        clk,       // clock signal
    input  wire        rst_n,     // reset signal
    input  wire [7:0]  ui,        // inputs from ui[0] to ui[7]
    output wire [7:0]  uo,        // outputs uo[0] to uo[7]
    inout  wire [7:0]  uio        // bidirectional pins uio[0] to uio[7]
);

    reg [7:0] count;

    // You can use ui[0] as enable, ui[1] as load, ui[2:9] as load_value or however you want to map inputs
    wire enable = ui[0];
    wire load   = ui[1];
    wire [7:0] load_value = ui; // Or ui[7:0] if you want all inputs to be load_value

    // Asynchronous reset and synchronous load
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'd0;
        else if (load)
            count <= load_value;
        else if (enable)
            count <= count + 1;
    end

    // Output logic:
    assign uo = count;

    // For bidirectional uio pins, you can just keep them as inputs or outputs depending on your design.
    // Here, let's just drive them as outputs equal to count:
    assign uio = count; // Or set as high impedance if not driven: assign uio = 8'bz;

endmodule
