module fir_filter_top(
    input logic clk,
    input logic rst_n,                  // rst"_n" means we are using active low reset
    input logic signed [15:0] data_in 
);
logic signed [15:0] x_reg [0:46];       // 47 value window, 47 "taps"
logic signed [15:0] coeff_regs [0:23];
logic signed [16:0] pre_add_regs [0:22];     // 17'b; holds 23 values (0-22, 24-46), index 23 is the center
logic signed [32:0] product_regs [0:23];     // 33'b = (17'b sum) * (16'b Q1.15 float)     


always_ff @(posedge clk or negedge rst_n) begin : main
    // Module Definition & Shift Register Array
    if (!rst_n) begin                   // reset: everything goes to zero
            for (int i = 0; i < 24; i++) coeff_regs[i] <= 16'sh0000;
            for (int i = 0; i < 47; i++) x_reg[i] <= 16'sh0000;
        end 
    else begin                          // NOT reset, shift by one (take in new datapoint)
        x_reg[0] <= data_in;
        for (int i = 1; i < 47; i++) begin
            x_reg[i] <= x_reg[i-1];
        end
    end

    // Pipelined Pre-Adder & Multiplier Layer
    for (int i = 0; i <23; i++) begin
        pre_add_regs[i] <= x_reg[i] + x_reg[46-i];
        
    end

    end

endmodule