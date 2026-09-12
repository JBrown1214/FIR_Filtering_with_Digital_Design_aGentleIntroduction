module fir_filter_top_tb(output data_out);

    `timescale 1ns / 10ps

    // 25Mhz = 25e6 hz = Frequency
    // Frequency = 1 / Period
    // clock period = 1/25e6 seconds = 1000/25 ns = 40ns

    localparam time CLK_PERIOD = 40ns;
    logic clk = 0;

    // Toggle every half period
    always #(CLK_PERIOD / 2) clk = ~clk;

    reg signed [15:0] stimulus_mem [0:4999];
    reg signed [15:0] gold_standard_mem [0:4999];


    initial begin
        $readmemh("C:/Users/johnn_erba506/Documents/Git/FIR_RTL/RTL_Architecture/messy_stimulus.hex", stimulus_mem);
        $readmemh("C:/Users/johnn_erba506/Documents/Git/FIR_RTL/RTL_Architecture/expected_output.hex", gold_standard_mem);
    end
    integer out_index = 0;
    integer error_count = 0;

    always @(posedge clk) begin
        if (out_index < 20) begin
            // Account for pipeline latency shift when checking against golden model
            if (out_index >= 4) begin
                if (data_out !== gold_standard_mem[out_index - 4]) begin
                    $display("MISMATCH Error at sample %d: Expected %h, Got %h", 
                            out_index, gold_standard_mem[out_index - 4], data_out);
                    error_count = error_count + 1;
                end else begin 
                    $display("----success: index %d holds ----", out_index);
                end
            end
            out_index = out_index + 1;
        end
    end

endmodule