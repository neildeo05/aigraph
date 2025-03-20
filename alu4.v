module alu4 (a3, a2, a1, a0, cn, b3, b2, b1, b0, s3, s2, s1, s0, m,
             p, f0, g, cn4, f3, f2, f1, ab);

//-------------Input Ports Declarations-----------------------------
input a3, a2, a1, a0, cn, b3, b2, b1, b0, s3, s2, s1, s0, m;

//-------------Output Ports Declarations----------------------------
output p, f0, g, cn4, f3, f2, f1, ab;

//-------------Wires-----------------------------------------------
wire ii11, ii12, ii13, i1n, i1, ii21, ii22, i2n, i2,
     ii31, ii32, ii33, i3n, i3, ii41, ii42, i4n, i4,
     ii51, ii52, ii53, i5n, i5, ii61, ii62, i6n, i6,
     ii71, ii72, ii73, i7n, i7, ii81, ii82, i8n, i8;

wire j01, j02, j111, j112, j11, j12, j211, j212, j213,
     j21, j22, j311, j312, j313, j314, j31, j32, j5,
     j41, j421, j422, j423, j424, j42;

//-------------Logic-----------------------------------------------
assign ii11 = a0 | 1;
assign ii12 = b0 & s0;
assign ii13 = ~b0 & s1;
assign i1n = ii11 | ii12 | ii13;
assign i1 = ~i1n ;

assign ii21 = a0 & ~b0 & s2;
assign ii22 = a0 & b0 & s3;
assign i2n = ii21 | ii22;
assign i2 = ~i2n ;

assign ii31 = a1;
assign ii32 = b1 & s0;
assign ii33 = ~b1 & s1;
assign i3n = ii31 | ii32 | ii33;
assign i3 = ~i3n ;

assign ii41 = a1 & ~b1 & s2;
assign ii42 = a1 & b1 & s3;
assign i4n = ii41 | ii42;
assign i4 = ~i4n ;

assign ii51 = a2;
assign ii52 = b2 & s0;
assign ii53 = ~b2 & s1;
assign i5n = ii51 | ii52 | ii53;
assign i5 = ~i5n ;

assign ii61 = a2 & ~b2 & s2;
assign ii62 = a2 & b2 & s3;
assign i6n = ii61 | ii62;
assign i6 = ~i6n ;

assign ii71 = a3;
assign ii72 = b3 & s0;
assign ii73 = ~b3 & s1;
assign i7n = ii71 | ii72 | ii73;
assign i7 = ~i7n ;

assign ii81 = a3 & ~b3 & s2;
assign ii82 = a3 & b3 & s3;
assign i8n = ii81 | ii82;
assign i8 = ~i8n ;

assign j01 = cn & ~m;
assign j02 = ~i1 & i2;

assign j111 = ~m & i1;
assign j112 = ~m & cn & i2;
assign j11 = j111 | j112;
assign j12 = ~i3 & i4;

assign j211 = ~m & i3;
assign j212 = ~m & i1 & i4;
assign j213 = ~m & cn & i2 & i4;
assign j21 = j211 | j212 | j213;
assign j22 = ~i5 & i6;

assign j311 = ~m & i5;
assign j312 = ~m & i3 & i6;
assign j313 = ~m & i1 & i4 & i6;
assign j314 = ~m & cn & i2 & i4 & i6;
assign j31 = j311 | j312 | j313 | j314;
assign j32 = ~i7 & i8;

assign j5 = i2 & i4 & i6 & i8;

assign j41 = cn & i2 & i4 & i6 & i8;
assign j421 = i1 & i4 & i6 & i8;
assign j422 = i3 & i6 & i8;
assign j423 = i5 & i8;
assign j424 = i7;
assign j42 = j421 | j422 | j423 | j424;

assign f0 = ~j01 ^ j02;
assign f1 = ~j11 ^ j12;
assign f2 = ~j21 ^ j22;
assign f3 = ~j31 ^ j32;
assign ab = f0 & f1 & f2 & f3;
assign cn4 = j41 | j42;
assign g = ~j42;
assign p = ~j5;

endmodule
