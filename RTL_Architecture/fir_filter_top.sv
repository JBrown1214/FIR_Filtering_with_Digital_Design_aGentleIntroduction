module fir_filter_top(
    input logic clk,
    input logic rst_n,                      // rst"_n" means we are using active low reset
    input logic signed [15:0] data_in, 
    output logic signed [15:0] data_out           // Q1.15 * 1
);
/*============ a note on notation ============
    I am using Q number formatting (see: https://en.wikipedia.org/wiki/Q_(number_format))
    
    More specifically: I am using ARM style Q number formating. 

    All Q number formats use "U" sign bits (-2^0), "m" integer bits (2^m), and "n" fractional bits (2^-n)
    To quote wikipedia: 
        """
        The Q notation... consists of the letter Q followed by a pair 
        of numbers m.n, where m is the number of bits used for the integer part of the value, 
        and n is the number of fraction bits.

        By default, the notation describes signed binary fixed point format, with the unscaled integer 
        being stored in two's complement format, used in most binary processors. As such, the first bit 
        always gives the sign of the value (1 = negative, 0 = non-negative), and it is not counted
        in the m parameter. Thus, the total number w of bits used is 1 + m + n.

        In particular, when n is zero, the numbers are just integers. If m is zero, all bits except the 
        sign bit are fraction bits; then the range of the stored number is from −1.0 (inclusive) to +1.0 (exclusive).
        """

    According to the ARM variant of Q notation, the sign bit and integer bit(s) are added together
        e.g. Q1.15 is 1 sign bit  + (0 integer bits) + 15 fractional bits (2^-1 through 2^-15).
============================================*/

// 47 taps + 24 coefficients (1 coeff for each pair + 1 coeff for the middle value at index 23)
logic signed [15:0] x_reg [0:46];           // Q1.15
logic signed [15:0] coeff_regs [0:23];      // Q1.15

// 23 17'b pre_add registers to store the result of the inital "halving" addition (extra bit is 2^0 overflow)
logic signed [16:0] pre_add_regs [0:23];    // Q2.15: 1`sign + 1'overflow + 15'fracb

// 24 33'b product registers to store the result of the float multiplication (pre-add * coeff)
    // pre-add = 17'b: 1'sign + 1'overflow + 15'fracb
    // coeff = 16'b: 1'sign + 15'fracb
    // pre-add * coeff = 1'sign + 2' overflow + 30'fracb
    // (2' of overflow is required in the case of -2 * -1 = 2)
logic signed [32:0] product_regs [0:23];    // Q3.30: 1'signb + 2'intoverflow + 30'fracb)

// registers for each clock cycle of the pipeline accumulator
// we need to add an overflow bit for every addition to safeguard the theoretical worst case. 
logic signed [33:0] Accum_reg_24to12 [0:11];// Q4.30 * 12
logic signed [34:0] Accum_reg_12to6 [0:5];  // Q5.30 * 6
logic signed [35:0] Accum_reg_6to3 [0:2];   // Q6.30 * 3
logic signed [36:0] Accum_reg_3to2 [0:1];   // Q7.30 * 1 + Q6.30 * 1 (reg for both vals is needed for pipeline)
logic signed [37:0] Accum_reg_2to1;         // Q8.30 * 1 


always_ff @(posedge clk or negedge rst_n) begin : main
    
    //* ==========Reset Logic==========
    if (!rst_n) begin
            for (int i = 0; i < 47; i++) x_reg[i] <= 16'sh0000;
            for (int i = 0; i < 24; i++) coeff_regs[i] <= 16'sh0000;
            for (int i = 0; i < 24; i++) pre_add_regs[i] <= 17'sh0000;
            for (int i = 0; i < 24; i++) product_regs[i] <= 33'sh0000;
            for (int i = 0; i < 12; i++) Accum_reg_24to12[i] <= 34'sh0000;
            for (int i = 0; i < 6; i++)  Accum_reg_12to6[i] <= 35'sh0000;
            for (int i = 0; i < 3; i++)  Accum_reg_6to3[i] <= 36'sh0000;
            for (int i = 0; i < 2; i++)  Accum_reg_3to2[i] <= 37'sh0000;
            Accum_reg_2to1 <= 38'sh0000;
            data_out <= 16'sh0000;
        end 
    else begin
        //* ==========data_in Shift Register Array (1 clock)==========
        x_reg[0] <= data_in;
        for (int i = 1; i < 47; i++) begin      // shift by one (take in new datapoint)
            x_reg[i] <= x_reg[i-1];
        end
        // ======================================================================
        //* ==========Pipelined Pre-Adder & Multiplier Layer (3 clocks)==========
        // ======================================================================

        //PRE_ADD       (Q1.15 + Q1.15 == Q2.15)
        for (int i = 0; i <23; i++) begin : Pre_Adder      
            pre_add_regs[i] <= x_reg[i] + x_reg[46-i];
        end
        pre_add_regs[23] <= 17'(x_reg[23]);          // keep x[23] in-time with other x_reg values (not a clock behind)

        // MULTIPLY     (Q2.15 * Q1.15 == Q3.30)
        for (int i = 0; i <24; i++) begin : Multiplier      
            product_regs[i] <= pre_add_regs[i] * coeff_regs[i];
        end

        // ===========================================================
        //* ==========Pipelined Accumulator Layer (5 clocks)==========
        // ===========================================================

        // 24 values --clk1-> 12val --clk2-> 6v --clk3-> 3v --clk4-> 2v --clk5-> 1 value
        for (int i = 0; i < 12; i++) begin : Accum24to12    // Q3.30 + Q3.30 == Q4.30
            Accum_reg_24to12[i] <= product_regs[i] + product_regs[23-i];
        end
        for (int i = 0; i < 6; i++) begin : Accum12to6      // == Q5.30
            Accum_reg_12to6[i] <= Accum_reg_24to12[i] + Accum_reg_24to12[11-i];
        end
        for (int i = 0; i < 3; i++) begin : Accum6to3       // == Q6.30
            Accum_reg_6to3[i] <= Accum_reg_12to6[i] + Accum_reg_12to6[5-i];
        end
        
        // Accum_reg_3to2: Q7.30 == Q6.30 + Q6.30 
        Accum_reg_3to2[0] <= Accum_reg_6to3[0] + Accum_reg_6to3[1];
        Accum_reg_3to2[1] <= {Accum_reg_6to3[2][35],Accum_reg_6to3[2]}; // arithmetic sign extension
        
        // Accum_reg_2to1: Q8.30 == Q7.30 + Q7.30
        Accum_reg_2to1 <= Accum_reg_3to2[0] + Accum_reg_3to2[1];    // Q8.30
        
        // Q8.30 == 1 bit sign [37]; 7 bits int [36:30]; 30 bits fractional [29:0] 
        // Q1.15 == 1 bit sign [0], 15 bits fractional[14:0].
        // data out (Q1.15) == Q8.30[37]; Q8.30[29:15]
        data_out <= {Accum_reg_2to1[37], Accum_reg_2to1[29:15]};
    end
end

endmodule