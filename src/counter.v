module counter (
    input  wire        clk,
    input  wire        rst_n,       // asynchronous active-low reset
    input  wire        load,        // synchronous load enable
    input  wire [7:0]  load_value,  // value to load when load is high
    input  wire        enable,      // counter enable
    input  wire        oe,          // output enable (active high)
    output wire [7:0]  q            // tri-state output
);

    reg [7:0] count;

    // Asynchronous reset and synchronous load
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'd0;
        else if (load)
            count <= load_value;
        else if (enable)
            count <= count + 1;
    end

    // Tri-state output
    assign q = (oe) ? count : 8'bz;

endmodule
