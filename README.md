# War (Card Game) Simulator

After a seemingly un-ending game of the card game War with my daughter, we asked the important questions:

* Can a game of War theoretically go on forever?
* How long is the average game of War?

Some [smart folks](https://arxiv.org/abs/1007.1371) already answered that - it is finite. But I like to code
so I thought I'd try to get some stats about an average game of War with a simple Python simulator.

## Game Rules

The rules of the game are simple enough it can be fully automated.

 * [Bicycle Cards Rules](https://bicyclecards.com/how-to-play/war/)
 * [Wikipedia Rules](https://en.wikipedia.org/wiki/War_(card_game))
 
# Summary

After running about a million rounds of War in the simulator - the stats
were pretty well converged to the values in the table below. The shortest
and longest games there are not theoretical values - just observations. 

It is possible to win in 1 round if it is an epic series of ties, and it is
possible for a game to go on for much longer than 5000 rounds if you are very unlucky.

| Stat  | Value |
|-------|-------|
| Average length |  440-445 rounds |
| Median length  |  330-335 rounds |
| Longest game   | ~5000 rounds    |
| Shortest game  | 18 rounds       |
| 95% game length | 1160 rounds   |
| 99% game length | 1750 rounds   |
| 99.9% game length | 2600 rounds |