# champions-league-monte-carlo
CHAMPIONS LEAGUE DRAW 22/23 MONTE CARLO SIMULATOR

The Champions League is football's most prestigious club competition.
The knockout stage draw presents a rather interesting probability problem, so I
wrote a Monte Carlo simulator for it.

THE MATH:

This particular draw is for the Round of 16 stage, because it becomes much less
interesting after that. In the Round of 16 draw, the 16 qualified teams are
split into two groups: the 8 teams that won their group (seeded) and the 8
teams that came second in their group (unseeded) in the previous stage. The
draw will match up a seeded team with an unseeded team. However, there are two
major technicalities that make the probabilities rather complex:

1. There are restrictions on which teams can play each other. Two teams from
the same group or the same country cannot play each other! This restriction is
removed in later rounds, which is why the R16 draw is far more interesting.

Further, exactly one team comes from the same group (as a result of the rules
of qualification from the group stage), but there can be any number of teams
from the same country.

2. The pairings are chosen one-by-one, and in a random order. This part is
traditionally done manually: as part of a ceremony, someone will pick a ball
at random for the unseeded team in the pairing, then again for the seeded team.
The pool of options (in practice, balls in the bowl) is determined by whoever
is yet to be drawn such that that option will not make the rest of the draw
impossible.

This leads to some rather interesting situations and probabilities.

For instance, consider the following situation: 8 teams have already been drawn
(4 from each pot). Let's say the following are left:

UNSEEDED: A B C D
SEEDED:   E F G H

Then suppose that these are the only options that are not eliminated by same
group or country:

A:     B:  C:     D:
F G H  F   E G H  E F G

Since B can only be paired with F, none of the other teams will be paired with
F to prevent a deadlock. So then the options become the following:

A:   C:     D:
G H  E G H  E G

B is taken out for simplicity, since regardless of when it is drawn, it will be
paired with F. Crucially, since the draws are done one-by-one, the
probabilities are NOT 50/50, 33/33/33, and 50/50 respectively.

Only one pairing's probability will be described for an example: A and G. It
appears to be 50%, but it in fact is not.

There is a 1/3 probability that A is drawn first, then a further 1/2
probability that G is drawn next, yielding a 1/6 probability in one outcome.

There is a 1/3 probability that C is drawn first, then a further 1/3
probability that H is drawn next. A's only remaining option would be G,
yielding a 1/9 probability in one outcome.

If C is drawn first then draws G, trivially A-G is impossible. However, if C
draws E, then D's only remaining option is G, also locking out A-G.

Finally, there is a 1/3 probability that D is drawn first, then a further 1/2
probability that E is drawn next. Whichever of A and C is drawn next, there is
a further 1/2 probability that A and G are paired, yielding a 1/6 probability
in this outcome.

Of course, if D draws G, then A-G is impossible.

Adding up each relevant outcome, there is a 1/6 + 1/9 + 1/6 = 4/9 probability
(or approximately 44%) that A will pair with G at this stage. Despite A having
3 valid opponents, and 2 that are actually possible, the probability for this
pair is neither 1/2 nor 1/3. Essentially, it is not uniform.

Naturally, the probabilities become much more complex with 8 teams in each pot.
Technically, there are approximately (8!)^2 possible paths! (Of course, the
actual computational size can be reduced significantly with dynamic
programming)

THE PROGRAM:

I wanted to experiment with Monte Carlo simulation. This is a simple enough
problem that it could be exactly solved with a conditional tree, but this is
just for fun, so I decided to do it experimentally. Maybe one day I will also
write the exact conditional tree version, it would be a similar dynamic
programming problem.

On the user end, the program will only request the following: whether to use
past dynamic data, how many simulations to perform, and whether to overwrite
the dynamic data file. Each simulation will simulate one Champions League
draw, pairing unseeded and seeded teams one-by-one (unseeded team first, just
like the actual draw goes). The only tricky part is testing whether a certain
pairing will eventually result in a lock---this is ultimately done by
recursively testing every possible pairing after and returning as soon as a
viable path is found. A cache was added, essentially dynamic programming, to
avoid repeating tests of the same path. Further, using the pickle library, this
cache can be saved at the end of the program and loaded at the start. Provided
that "cldynamicdata.pkl" is loaded at the start, the program will even update
the past data, but if it is not loaded at the start, it will completely
overwrite with the data from the current trial (either way, this only occurs if
the user agrees to write/overwrite the file).

In the end, the program will print the estimated probabilities of each pairing
in a table. 10000 simulations will usually take about 10 seconds without past
data, and after enough simulations, if the dynamic data is continually updated,
it can come down to about 5 seconds. In practice, it was in fact even lower,
but of course, processing time is different on every device.
