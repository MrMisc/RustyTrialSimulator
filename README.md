# RustyTrialSimulator

We assembled an advanced trial simulator.  We made it at a client's request to demonstrate how no typical user behaviour impacts the outcome of trials. 

In particular, there is no quantifiable difference between "attempting" trials at a fixed rate per session and coming back versus choosing to end each session once a certain number of failures has been reached. 

By default, this system implies a system whereby failure at a trial, excluding the original one, leads to the user falling to the previous shot.  This can be adjusted when inputting the probability string representing the trials' probabilities by appending them with a * respectively.  Additional parameters, such as k,j, and h, have been added for specific trials of the user's desire.  These trials call the user to fall to the first, second and third trials.  Suffixing a T also allows the user to represent a trial that causes the user to fall by two levels instead!

The user also asks for a money scheme for each trial in particular.

## Methods | Brief description

Methods represent a mixture of user behaviour and trial features. 

1-10 represent trials whereby a pity system is incorporated.  Specifically, two successive trial failures lead to an automatic success in the subsequent trial attempt. 

However, methods 1-4 do not permit the pity system to trigger at * levels.  A repeated failure at the fixed levels is not qualifiable for a pity win afterwards for the methods!  The trials at which the user has failed must be distinct.

### Method Rubric

%1: represents the user attempting a fixed number of attempts to stop and restart attempts from where they left off.

%2: represents a failure-averse method where the seed/user quits upon a specified number of failures achieved.

%3: a hybrid of the 2.  Once %1 fails, a %2 is activated.

%4-%0: No current method.
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



## **Consideration

Considering adding new set of methods 20-39 that would, instead of innately providing a pity system whereby the user gets a free win in the current trial given that the previous distinct 2 have been failed at. 

* What if we instead(20-29) or in addition(30-39) rewarded successive successes?
* What if we adjusted the number of trials that trigger this free win?
* What if we adjusted the original pity system to be adjustable as well? For instance, instead of 2 distinct failures, consider 3 successive failures?


