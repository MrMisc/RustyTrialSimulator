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

