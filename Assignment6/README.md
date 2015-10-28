#Bayes Net

usage: baesnet.py [-h] [-d] [-c C] [-j J] [-m M] [-p P P] input_file

positional arguments:
  input_file  text file specification of the network

optional arguments:

  -h, --help  show this help message and exit

  -d          show distributions

  -c C        conditional probability

  -j J        joint probability

  -m M        marginal probability

  -p P P      set a priori or a cpt table entry

-----------
##input file
The input file parameterizes the network. Each line should describe an entry to the conditional
probability table of a node. A priori has no conditional dependencies (parents) and looks like:

P:0.4

A node with a conditional dependency is formatted as below and should be interpreted P(C|P) = .2 and P(c|P) = .8 is automatically assumed. Only True probabilities should be specified. All complements are inferred.

C/P:0.2

A nodes with muliple conditional dependencies may take comma separated parents:

D/P,A:0.3

This Bayesian implementation only works with binary random variables. The true state is denoted with a 
capital letter and the false state corresponds to the lower case letter. For example, from the above examples, 
one must specify both.

C/P:0.2

C/p:0.2

For a node with 2 parents, we note that the number of lines to specify the conditional probability table is parents^2

D/P,A:0.001

D/P,a:0.23

D/p,A:0.99

D/p,a:0.073


##Example queries

#### Marginal of C
`python baesnet.py baesnet.txt -m C`

Computes P(C)

#### Quickly changing priori
`python baesnet.py baesnet.txt -p S .7 -m C`
 
#### Or changing other CPT entries
`python baesnet.py baesmet.txt -p C/S,p .89 -m C`

#### Conditional probabilties
`python baesnet.py baesnet.txt -c S/X`

Computes P(S|X)

#### The show distribution flag
`python baesnet.py baesnet.txt -d -m C`

Adding the -d option will show the calculations involved.


P(SPC)
= P(C|P,S) * P(S) * P(P)
= 0.05 * 0.3 * 0.1

P(SpC)
= P(C|S,p) * P(S) * P(p)
= 0.03 * 0.3 * 0.9

P(sPC)
= P(C|P,s) * P(s) * P(P)
= 0.02 * 0.7 * 0.1

P(spC)
= P(C|p,s) * P(s) * P(p)
= 0.001 * 0.7 * 0.9

P(C)
= P(SPC) + P(SpC) + P(sPC) + P(spC)
= 0.0015 + 0.0081 + 0.0014 + 0.00063
= 0.011630
