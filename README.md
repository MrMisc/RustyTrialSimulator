# RustyTrialSimulator

We assembled an advanced trial simulator.  We made it at a client's request to demonstrate how no typical user behaviour impacts the outcome of trials. 

In particular, there is no quantifiable difference between "attempting" trials at a fixed rate per session and coming back versus choosing to end each session once a certain number of failures has been reached. 

By default, this system implies a system whereby failure at a trial, excluding the original one, leads to the user falling to the previous shot.  This can be adjusted when inputting the probability string representing the trials' probabilities by appending them with a * respectively.  Additional parameters, such as k,j, and h, have been added for specific trials of the user's desire.  These trials call the user to fall to the first, second and third trials.  Suffixing a T also allows the user to represent a trial that causes the user to fall by two levels instead!

The user also asks for a money scheme for each trial in particular.

More information on the additional functionalities for this programme are available @ https://github.com/MrMisc/Rust-Modern-Trial-Simulator as well.

## Methods | Brief description

Methods represent a mixture of user behaviour and trial features. 

1-10 represent trials whereby a pity system is incorporated.  Specifically, two successive trial failures lead to an automatic success in the subsequent trial attempt. 

However, methods 1-4 do not permit the pity system to trigger at * levels.  A repeated failure at the fixed levels is not qualifiable for a pity win afterwards for the methods!  The trials at which the user has failed must be distinct.

(NEW!) Methods 100+: Methods that simulate a positive reinforcement system in place or in tandem with a pity system (look at rubric below for more details). A
reinforcement system is one whereby a consecutive set of successes is congratulated with an automatic win in the next trial. An interesting consideration worth
noting in trial design/rng design etc. What is more potent in driving or hindering success - the pity system or the reinforcement system?

### Method Rubric

The starting logic for methods was initially as below...

%1: represents the user attempting a fixed number of attempts to stop and restart attempts from where they left off.

%2: represents a failure-averse method where the seed/user quits upon a specified number of failures achieved.

%3: a hybrid of the 2.  Once %1 fails, a %2 is activated.

%4-%0: No current method.

#### Quick calibrations | using methods

The above is not invalidated to a significant extent, however, there is some underlying logic that is left not quite explained and/or explored in this method rubric. The less concerned user, should at the very least, note that within the methods 1-4, there is an underlying pity mechanism that is built into the simulator for these particular methods. The pity system activates a free 100% run on the current trial given that the user has previously failed 2 consecutive times. To avoid it, simply use methods 11-14 for the equivalent, without any pity system.

#### Additional Details

For the more curious user, here are some further details. As a preface, remember that by default, every level given by the user as a probability vector and price vector, is set to cause each simulation/seed to fall down to the previous trial level a level upon failure.

Firstly, the pity system does in fact trigger upon 2 consecutive failures. This, however, triggers only if the trials are unique. Hence, nothing happens if you fail on the same level twice. When does that happen - when falling below the trial level is impossible.  This in turn happens due to 2 reasons: you are at the first level, OR you have annotated a fixed level somewhere within the probability vector aside from the first level. This, is done by annotating the probability value for that trial level, with a * (eg 0.3,0.3,0.3*,0.3,0.3*).

Secondly, the pity system by default is set to such that it DOES NOT trigger at the fixed levels if you have failed twice at that level. However, the option to do so is available for any methods that are greater than or equal to 5 (for methods below 100). For methods above 100, take note that we have applied a similar logic to %100 < 5. In other words, 100-104, 200-204 etc. we are setting the pity system to only occur for unique failures, and not repeated ones at fixed levels, including the starting level. Everything else has that consideration removed, and the pity system, if validated, is triggered at the fixed levels as well even if fails are repeated there.

In addition to this, the option to REMOVE the pity system is available by simply making sure that %100>=10. Hence, methods 10-99, 110-199, 210-299 etc are methods that are not using the pity system. Failing 2 times in a row in any scenario with these methods inputted into the trial simulator will NOT trigger any pity system.

Finally, as we have begun mentioning them, there are now methods that are above 100 (the 100+ series). Initially, by design, methods past 15 were redundant. However, in the interest of examining **reinforcement** systems, we added them in. Essentially, methods above 100, reward the seed for succeeding a consecutive number of times. The number of times is decided by the ones digit of the method number (as long as it is >100) i.e. method_number%10 = N. Hence, this goes up to 9.

One may ask, does this replace the user behaviour initially coded for methods 1-3,11-13 for methods above 100? In fact, no! We have simply moved that logic to be denoted by the whole number division by 100. Hence, now method 102 for instance, denotes user behaviour reminiscent of method 1, WITH a pity system, AND a reinforcement system whereby the seed gets a free trial success after having completed 2 trial success in succession. The logic is as follows below...



| Primary<br>method | User behaviour                                                                                                                                                                                                                                                                                                                  | Pity system (2 fails)                                 | Reinforcement System (N successes)                                                                                                           | Explicit Conditions                                                                                                                                                                                                                         | Method Numbers<br> (user input)            |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| 1                 | Multiple attempts per seed to finish<br><br>Terminate each attempt at fixed number of attempts                                                                                                                                                                                                                                  | Yes<br><br>Does NOT apply at (*)<br>fixed boundaries  | No                                                                                                                                           | method_number%10 = 1<br><br>method_number<100<br><br>Method number must be<br>below 100 and have 1<br>in the ones place                                                                                                                     | 1                                          |
| 2                 | Multiple attempts per seed to finish<br><br>Terminate each attempt at fixed number of failures<br>accumulated                                                                                                                                                                                                                   | Yes<br><br>Does NOT apply at (*)<br>fixed boundaries  | No                                                                                                                                           | method_number%10 = 2<br><br>method_number<100<br><br>Method number must be <br>below 100 and have 2<br>in the ones place                                                                                                                    | 2                                          |
| 3                 | Multiple attempts per seed to finish<br><br>Terminate each attempt after fixed number attempts <br>UNLESS attempt has resulted in a net positive increment<br>in level on series of successive trials. At that point<br>, use method 2 logic and stop only after receiving a <br>fixed number of failures (falsecap parameter). | Yes <br><br>Does NOT apply at (*)<br>fixed boundaries | No                                                                                                                                           | method_number%10 = 3<br><br>method_number<100<br><br>Method number must be <br>below 100 and have 3<br>in the ones place                                                                                                                    | 3                                          |
| 4                 | None                                                                                                                                                                                                                                                                                                                            | Yes <br><br>Does NOT apply at (*)<br>fixed boundaries | No                                                                                                                                           | method_number%10 = 4<br><br>method_number<100<br><br>Method number must be<br>below 100 and have 4<br>in the ones place                                                                                                                     | 4<br>14<br>24<br>...<br><br>94             |
| 5-9               | None                                                                                                                                                                                                                                                                                                                            | Yes<br><br>DOES apply at (*) <br>fixed boundaries     | No                                                                                                                                           | method_number<100<br><br>Pity system allocation<br>method_number%100<10<br><br>!(method_number%10=1,2,3)<br><br>Method number must <br>not follow the above <br>patterns but be below<br>100. Also does not fall<br>under previous criteria | 5-9                                        |
| 10                | None                                                                                                                                                                                                                                                                                                                            | No                                                    | No                                                                                                                                           | Remaining in the tens                                                                                                                                                                                                                       | 10<br>20<br>30<br>...<br>90                |
| 11 (1)            | Multiple attempts per seed to finish<br><br>Terminate each attempt at fixed number of attempts                                                                                                                                                                                                                                  | No                                                    | No                                                                                                                                           | Same as Method 1                                                                                                                                                                                                                            | 11<br>21<br>31<br>...<br>91                |
| 12 (2)            | Multiple attempts per seed to finish<br><br>Terminate each attempt at fixed number of failures<br>accumulated<br>                                                                                                                                                                                                               | No                                                    | No                                                                                                                                           | Same as Method 2                                                                                                                                                                                                                            | 12<br>22<br>...<br><br>92                  |
| 13 (3)            | Multiple attempts per seed to finish<br><br>Terminate each attempt at fixed number of attempts <br>UNLESS attempt has resulted in net positive increment.<br>At that point, use method 2 logic.                                                                                                                                 | No                                                    | No                                                                                                                                           | Same as Method 3                                                                                                                                                                                                                            | 13 <br>23<br>...<br><br>93                 |
| %4-%9             | None                                                                                                                                                                                                                                                                                                                            | No                                                    | No                                                                                                                                           | method_number<100                                                                                                                                                                                                                           | 14,15..20<br>24,25..30<br>...<br>94,95..99 |
| 100-109           | Method 1;<br><br>Multiple attempts per session<br><br>Terminate each attempt at fixed number of attempts                                                                                                                                                                                                                        | Yes                                                   | Yes<br><br>Automatic successful trial upon <br>N successful trials in a row<br><br>N is the value of the first digit<br>of the method number | Condition<br>N = method_number%100<br><br>Reinforcement series<br>method_number>=100<br><br>User behaviour<br>method_number/100=1<br><br>Pity system<br>method_number%100<10                                                                |                                            |
| 110-199           | Method 1;<br><br>Multiple attempts per session<br><br>Terminate each attempt at fixed number of attempts                                                                                                                                                                                                                        | No                                                    | Yes                                                                                                                                          | Condition<br>N = method_number%100<br><br>Reinforcement series<br>method_number>=100<br><br>User behaviour<br>method_number/100=1                                                                                                           |                                            |
| 200-209           | Method 2;<br><br>Multiple attempts per session<br><br>Terminate each attempt at fixed number of failures<br>accumulated                                                                                                                                                                                                         | Yes                                                   | Yes                                                                                                                                          | Condition <br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100<br><br>User behaviour <br>method_number/100=2<br><br>Pity system <br>method_number%100<10                                                            |                                            |
| 210-299           | Method 2;<br><br>Multiple attempts per session<br><br>Terminate each attempt at fixed number of failures                                                                                                                                                                                                                        | No                                                    | Yes                                                                                                                                          | Condition<br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100<br><br>User behaviour <br>method_number/100=2                                                                                                         |                                            |
| 300-309           | Method 3;<br><br>Multiple attempts per session<br><br>Terminate each attempt at fixed number of attempts<br>UNLESS attempt has resulted in net positive increment.<br>At that point, follow method 2 logic.                                                                                                                     | Yes                                                   | Yes                                                                                                                                          | Condition<br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100<br><br>User behaviour <br>method_number/100=3<br><br>Pity system <br>method_number%100<10                                                             |                                            |
| 310-399           | Method 3;<br><br>Multiple attempts per session <br><br>Terminate each attempt at fixed number of attempts<br>UNLESS attempt has resulted in net positive increment.<br>At that point, follow method 2 logic                                                                                                                     | No                                                    | Yes                                                                                                                                          | Condition<br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100<br><br>User behaviour<br>method_number/100=3                                                                                                          |                                            |
| 400-409           | None                                                                                                                                                                                                                                                                                                                            | Yes                                                   | Yes                                                                                                                                          | Condition <br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100<br><br>Pity system <br>method_number%100<10                                                                                                          |                                            |
| 410-499           | None                                                                                                                                                                                                                                                                                                                            | No                                                    | Yes                                                                                                                                          | Condition<br>N = method_number%100<br><br>Reinforcement series <br>method_number>=100                                                                                                                                                       |                                            |



This trial simulator was initially constructed entirely on Python, with some bugs.  Instead of perpetually fixing the model in a set of code that takes forever to process relatively large sample sizes, it was prudent to construct the code in a low-level language instead.  This enabled us to quickly pick out more bugs than possible with the initially lengthy execution times.  


## GUI

Customtkinter enables the user to interact with the underlying code written in Rust.  

![UI](https://user-images.githubusercontent.com/100022747/210150561-12c9a042-93a3-4972-a568-29cdbef98090.png)


## Interaction between Python and Rust 
The initializing GUI python file executes subprocess commands.  The output from Rust is conveniently pipelined to another recipient Python file instead of outputting potentially time-wasting data to another format.  In our case, CSV only sometimes reliably outputs data with over 50000 rows.  Nonetheless, the data was readable when we initially attempted it. 

## Output

3 graphs are outputted at the end of execution.

i.  Attempt plot: pair-wise comparison of histograms for the two simulations for the number of independent attempt sessions taken to achieve the success of all the trials.  Irrelevant for methods where %10 > 4.

![plot2](https://user-images.githubusercontent.com/100022747/210150567-d177f59d-d44b-4949-99ea-be7616cf6a85.png)


ii.  Tapdata plot: pair-wise histogram comparing the number of successes every N individual trial attempts ("taps")


![tapdataplot](https://user-images.githubusercontent.com/100022747/210150575-93ebbed7-6161-4294-97cf-505bef2e70d5.png)


iii.  Money plot: Cost distribution comparison between the 2 simulations.


![moneyplot](https://user-images.githubusercontent.com/100022747/210150580-0b819b5b-2b7b-4524-8ef8-264c196d9595.png)


### Multi-threading note

This code set uses 2 threads for simulations below 100000 trials for each simulation and 16 for above.  I may change it later to account for probability values and the number of trials.  A low probability value and a high number of trials are easily demanding and time-consuming to compute on just 2 parallel threads.

### Default outputting 

A simple plt.show() command is also outputted quickly showing a temporary but saveable joined output figure with the "tapdata" and "moneydata" plots.

![printedoutput](https://user-images.githubusercontent.com/100022747/210150615-231c7e84-88e4-42d5-8720-ff8a76d28f12.PNG)

For the brave ones who made it this far, not that this is anything revolutionary, this sample of 1million sample for EACH simulation (for which there were 2) took less than 10min! To be precise, it took 482.0229332s to execute the arithmetic on Rust's part. This would have taken far longer in Python only rendition, which I used to use myself!

### Scaling with increased iterations | Compared to Python


![pythonvsrust](https://user-images.githubusercontent.com/100022747/210150718-e260d266-2f07-4172-92fb-56e049be79c4.png)

Rust appears to at least be 1.6 times faster than Python in executing the simulations.  This timing dataset was for only 1 simulation at a time without any multi-threading on either side.


