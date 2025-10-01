module tt_um_ccjiaa_counter (
    input wire [7:0]  uio,         // for load value
    input wire [7:0] ui,            // for clock, reset, enable
    output wire [7:0] uo         // 8-bit output count value
);

    wire clk;
    wire rst_n;
    wire enable;
    reg [7:0] count;

    assign clk   = ui[0];
    assign rst_n = ui[1];
    assign enable = ui[2];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'd0;
        else if (uio)
            count <= uio
        else
            count <= count + 1;
    end

    assign uo = count;

endmodule
