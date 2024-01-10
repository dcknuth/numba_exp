# numba_exp
An experiment with Numba using day 16 from the Advent of Code

## Day16 Before
Part 1 ran in seven thousands of a second, so it might not see much improvement on its own. The second part needs to run a bunch of times to find a maximum, so we might be able to pre-compile, run in parallel or both. Its original run time is 1.532 seconds.
### Note
Numba did not want to run with Python 3.12 (which I use with VS Code) so I used it with Python 3.9 from Spyder where the non-Numba times were 0.009 and 4.643.

## With Numba @jit
### Note about dictionaries
Numba gave an error as the function that I tried to use it on used Python dictionaries. I could get around this and get it to run by using @jit(forceobj=True), but it increased the run time, a lot
### Note about @jit
I think I picked a pretty bad function to try to use Numba on. It is longer than a couple lines and uses a couple dictionaries. Also, when you solve a day of Advent of Code, you are done. However, from the [5-min guide](https://numba.readthedocs.io/en/stable/user/5minguide.html) it is best to use the just-in-time compiler on things that will get the same item given to it many times. This can occur, but I didn't have it in mind when I noted to try with this particular day.

## With Numba - Attempt Two
Part 2 of Day 16 does have a lot of loops the way I wrote it and if I re-write it a bit, I might be able to get it to be OK for the parallel=True option. I will give this a try as a seperate file.
Unfortunately, I could not get these loops to run in parallel and [this question](https://stackoverflow.com/questions/50744686/numba-typingerror-cannot-determine-numba-type-of-class-builtin-function-or) seems to say that I would have to get everything to work as numpy arrays first and that my partial conversion of just the local maximums would not be enough. You can see what did not work out in day16_numba2.py

### Final note
I tried one more, tiny loop with @jit (day16_numba3.py), but it really is very dependant on only having numpy items and nothing else.