# Final bounded audit of answer.md

The embedded Python 3 code block was extracted from `answer.md`, compared with
`verify_certificate.py`, and executed independently. The two programs are
identical modulo leading/trailing whitespace. Execution returned:

```
N1 (4, 6) 0
Np1 (4, 6) 9382/6561
n2 (4, 5) 25553/6561
Npstar (9, 12) 134561396/387420489
All exact polynomial certificates passed.
```

The definitions in equations (19) and (20) agree with the embedded code and
with independently constructed polynomial dictionaries from the earlier audit.
The Bernstein conversion, strictness of E0 using its positive (0,0)
coefficient, all required positive denominators, the derivative argument for
the cubic, and the deduction of omega > v_star^2 were rechecked.

The final comparison has the correct strict directions: Q2/x exceeds the
rational expression in (22), which exceeds alpha-beta*v by the cubic
certificate, and alpha-beta*v exceeds Q1/x. Hence Q>0 is impossible for
s>=1/3. The separately proved small-s inequality then yields R>0.

No mathematical or certificate issue was found. This was a bounded final
audit, with no additional research undertaken.
