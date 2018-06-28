Python Implementation of structural operational semantics for a simple functional language CoreML.

We implemented both big-step and small-step operational semantics based on substitution.

The grammar of CoreML is as follows:<br />

programs<br />
P  ::= M

expressions<br />
M ::= n | true | false<br />
&nbsp; &nbsp; &nbsp; | &nbsp; x | fun x -> M | M M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; let x = M in M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; M + M | M - M | M * M | M / M | M == M<br />
&nbsp; &nbsp; &nbsp; | &nbsp;  M != M | M > M | M >= M | M < M | M <= M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; if M then M else M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; while M do M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; ref M | ! M | M := M<br />
&nbsp; &nbsp; &nbsp; | &nbsp; M ; M | skip<br />

values<br />
V ::= n | true | false | l | skip | fun x -> M<br />
