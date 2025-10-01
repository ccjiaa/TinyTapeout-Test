module tt_um_ccjiaa_counter (
    input wire [7:0]  uio,         // for clock and reset
    output wire [7:0]  uo         // 8-bit output count value
);

    wire clk;
    wire rst_n;
    reg [7:0] count;

    assign clk   = uio[0];
    assign rst_n = uio[1];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'd0;
        else
            count <= count + 1;
    end

    assign uo = count;

endmodule
