module temp (a, b, sel, o1, o2);
    input a, b, sel;
    output o1, o2;
    assign o1 = (sel) ? a : b;
    assign o2 = a & b;
endmodule