extern crate serde;
extern crate serde_json;
// #[macro_use] extern crate json_derive;
use serde::Deserialize;
use serde_json::json;
// use std::error::Error;
use std::fs::File;
use std::fs::OpenOptions;
use std::io::Read;
use std::io::Write;
use std::time::{Duration, Instant};
use std::{fs, io, process};
//Note that Rust automatically lets true as i32 be case as 1 and false as 0 as i32. In other words, we could find the number of false instances

#[derive(Deserialize)]
pub struct Entry {
    simulation1: simulation,
    simulation2: simulation,
    trials: u64,
}

#[derive(Deserialize)]
pub struct simulation {
    method: u32,
    runs: u32,
    starting_point: i32,
    probability: Vec<String>,
    moneytree: Vec<f64>,
    falsecap: u32,
}

mod trial {
    use rand::distributions::Uniform;
    use rand::{thread_rng, Rng};

    pub fn trial(prob: f64) -> bool {
        let mut rng = thread_rng();
        let roll = Uniform::new(0.0, 1.0);
        let rollnumber: f64 = rng.sample(roll);
        rollnumber < prob
    }
    // Note that we are going to have to examine each run
    //This programme will require a pure list of probabilities for the listofprobs variable input
    // it is also going to need *s to indicate which levels are secure and insecure
    pub fn runs(
        method: u32,
        lastrun_orig: i32,
        listofprobs: Vec<&str>,
        money_tree: &[f64],
        money_in: f64,
        number_of_runs: u32,
        mut laststate_in: bool,
        mut secondlaststate_in: bool,
        falsecap: u32,
    ) -> (i32, u32, f64, bool, bool, bool) {
        let mut lastrun: i32 = lastrun_orig.clone(); //level you are at
        let terminate: i32 = listofprobs.len().try_into().unwrap();
        let mut money: f64 = money_in;
        let mut listoffixables: Vec<u32> = Vec::new();
        let mut listofprobs_f: Vec<f64> = Vec::new();
        let mut booms0: Vec<u32> = Vec::new();
        let mut booms1: Vec<u32> = Vec::new();
        let mut booms2: Vec<u32> = Vec::new();
        let mut boomclap: Vec<u32> = Vec::new();
        let mut countable: u32 = 0;
        for i in listofprobs {
            if i.contains("*") {
                listofprobs_f.push(
                    i.replace("*", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .parse::<f64>()
                        .unwrap(),
                );
                listoffixables.push(countable);
            } else if i.contains("k") {
                // if you fail, you fall to first level
                listofprobs_f.push(
                    i.replace("k", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .parse::<f64>()
                        .unwrap(),
                );
                booms0.push(countable);
            } else if i.contains("j") {
                // if you fail, you fall to second level
                listofprobs_f.push(
                    i.replace("j", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .parse::<f64>()
                        .unwrap(),
                );
                booms1.push(countable);
            } else if i.contains("h") {
                // if you fail, you fall to third level
                listofprobs_f.push(
                    i.replace("h", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .parse::<f64>()
                        .unwrap(),
                );
                booms2.push(countable);
            } else if i.contains("T") {
                // if you fail, you fall 2 levels -> to compoundly simulate boom stages that you can also fall from failing at
                listofprobs_f.push(
                    i.replace("T", "")
                        .replace(",", "")
                        .replace(" ", "")
                        .parse::<f64>()
                        .unwrap(),
                );
                boomclap.push(countable);
            } else {
                listofprobs_f.push(i.replace(",", "").replace(" ", "").parse::<f64>().unwrap());
            }
            countable += 1
        }
        //Assuming that we have transformed the string of probabilities here, let us continue with each trial run
        countable = 0; //reset countable to just record number of sit down rolls until termination of session
        let mut falsecount: u32 = 0;
        let mut f_star: bool = false;
        let mut series_true: u8 = 0; //for 100+ method series
        let mut falsecount_is_on: bool = true; //for method 3 class
        let over100par: u8 = (method%10) as u8; //last digit for 100+ series now instead denotes number of successive successes required to get free win
        loop {
            //Special condition for method 3 class
            if (method>100 && method/100==3) || (method<100 && method%10==3){
                falsecount_is_on = false;
            }            
            //breaking conditions
            if lastrun >= terminate {
                break;
            } else if method<100 && method % 10 == 1 && countable >= number_of_runs {
                break;
            } else if method>=100 && method/100 == 1 && countable >= number_of_runs{
                break;
            }else if method<100 && method % 10 == 2 && falsecount >= number_of_runs {
                break;
            } else if method>100 && method/100 == 2 && falsecount >= number_of_runs{
                break;
            }else if method<100 && method % 10 == 3 && countable >= number_of_runs && lastrun <= lastrun_orig {
                break;
            } else if method<100 && method % 10 == 3 && countable >= number_of_runs && lastrun > lastrun_orig {
                falsecount_is_on=true;
                if falsecount >= falsecap {
                    break;
                }
            }else if method>100 && method / 100 == 3 && countable >= number_of_runs && lastrun <= lastrun_orig {
                break;
            } else if method>100 && method / 100 == 3 && countable >= number_of_runs && lastrun > lastrun_orig {
                falsecount_is_on=true;
                if falsecount >= falsecap {
                    break;
                }
            } 
            //Methods 1-3 use * to denote 'unfallable' stages.
            let ref_lastrun: usize = lastrun.clone() as usize; //turning level parameter into usable index for vector
            money += money_tree[ref_lastrun];
            if !secondlaststate_in && !laststate_in && method%100 < 10 {//pity system: fail 2 times in a row, you go up. 
                //pity system revoked for methods above 9.
                //changed method < 10 to method %100 <10 to include user behaviours in "modified pity system automatic rewards" - 100+ series shall reward successive successes with 1 free win, and
                //100-109 this way should be including pity system where you fail twice leads to one free win
                laststate_in = true;
                secondlaststate_in = false;
                countable += 1;
                lastrun+=1;
                f_star=false;
            }else if method>=100 && series_true==over100par{ //success check system for method 100+
                series_true=0;//reset counter
                lastrun+=1; //auto success
                countable+=1;//counts as a roll as well

            } else {
                secondlaststate_in = laststate_in;
                laststate_in = trial(listofprobs_f[ref_lastrun]);
                if laststate_in {
                    //if level success AND it is not a compounding boom test level
                    //determine if this is on a compounding stage ("boom test")
                    lastrun += 1;
                    f_star = false;
                    if (booms0.contains(&(lastrun as u32))
                        || booms1.contains(&(lastrun as u32))
                        || booms2.contains(&(lastrun as u32)))
                        == false // given that the succeeded stage is not a boom stage
                    {
                        countable += 1; //This qualifying condition that it is not a success on the boom level is to ensure that we do not even 'count' that as an attempt. countable is merely an optical parameter, while lastrun increases anyway
                        //I also would now like to record progressive successes in case we are doing 100+ series
                        series_true+=1;
                    }
                } else if listoffixables.contains(&(lastrun as u32)) {//failed but on fixed level. ***BUT need to account for fact that we could be falling on here for the first time.
                    lastrun += 0;
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0; //you failed so this successive success parameter is set back to 0
                    //At this stage, the last roll laststate_in is a False on teh trial
                    //cheat the system and make sure pity system is not triggered at fixed stage (change second last state to true). Otherwise getting unlucky at fixed spot is exploited
                    //This is only to maintain the specific game scenario that we are depicting so lim to methods 1,2,3
                    if method < 5 && f_star{ //acounting for whether this is the first time we have touched this fixed level or not here is here
                        secondlaststate_in = true; //change second last roll log to true, to guard against a potential double fail pity system being triggered by failure at the 
                    }
                    f_star = true; // "we have failed on a fixed level in the last run" -> only reset if you succeed
                } else if booms0.contains(&(lastrun as u32)) {
                    lastrun = 0; //failed on critical stage, fall to first level
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                    //when you boom, there is no extra stage bonus from pity system
                    if method < 5 {
                        secondlaststate_in = true;
                    }
                } else if booms1.contains(&(lastrun as u32)) {
                    lastrun = 1; //similar but fall to second stage
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                    if method < 5 {
                        secondlaststate_in = true;
                    }
                } else if booms2.contains(&(lastrun as u32)) {
                    lastrun = 2;//3rd stage fall
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                    if method < 5 {
                        secondlaststate_in = true;
                    }
                } else if boomclap.contains(&(lastrun as u32)) {
                    //to compensate for the fact that we are using 2 stages in a compound manner to represent a trial with 3 outcomes instead of
                    lastrun -= 2;
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                } else if lastrun > 0 {
                    lastrun -= 1;
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                } else {
                    // lastrun += 0;
                    if falsecount_is_on{falsecount += 1;}
                    countable += 1;
                    series_true=0;
                    if method < 5 {
                        secondlaststate_in = true;
                    }
                }
            }
        }

        (
            lastrun,
            countable,
            money,
            laststate_in,
            secondlaststate_in,
            lastrun == terminate,
        )
    }
    //Let us create a fresh, simulator programme that we can simply call to run an atomic trial to iterative success! Only 1 trial though. Simulating multiple trials requires looping this!
    pub fn simulate(
        method: u32,
        number_of_runs: u32,
        starting_point: i32,
        listofprobs: Vec<&str>,
        money_tree: Vec<f64>,
        falsecap: u32,
    ) -> (i32, u32, f64) {
        let mut run_meter: i32 = 0; //starting value for lastrun_orig in runs
        let mut result_table: (i32, u32, f64, bool, bool, bool) =
            (starting_point, 0, 0.0, true, true, false);
        while !result_table.5 {
            let copied_listofprobs: Vec<&str> = listofprobs.clone();
            let copied_moneytree: &[f64] = &money_tree;
            //Below is an earlier version referencing to a function called result_table_addition. To try minimising time wasted referencing outside functions, I have attempted to nest the simple addition here
            // result_table = result_table_addition(result_table, runs(method, result_table.0, copied_listofprobs, copied_moneytree, result_table.2, number_of_runs, result_table.3, result_table.4, falsecap));
            let result_table2: (i32, u32, f64, bool, bool, bool) = runs(
                method,
                result_table.0,
                copied_listofprobs,
                copied_moneytree,
                result_table.2,
                number_of_runs,
                result_table.3,
                result_table.4,
                falsecap,
            );
            result_table = (
                result_table2.0,
                result_table.1 + result_table2.1,
                result_table2.2,
                result_table2.3,
                result_table2.4,
                result_table2.5,
            ); //only addition here is to add the number of rolls taken inside the countable output var
            run_meter += 1;
        }
        (run_meter, result_table.1, result_table.2) //(number of sessions, number of taps, money spent)
    }

    pub fn simulate_doublethread(
        method: [u32; 2],
        number_of_runs: [u32; 2],
        starting_point: [i32; 2],
        listofprobs: [Vec<&str>; 2],
        money_tree: [Vec<f64>; 2],
        falsecap: [u32; 2],
    ) -> [(i32, u32, f64); 2] {
        use std::sync::{Arc, Mutex};
        use std::thread;
        let prob1 = Arc::new(Mutex::new(listofprobs[0].clone()));
        let prob2 = Arc::new(Mutex::new(listofprobs[1].clone()));
        let money1 = Arc::new(Mutex::new(money_tree[0].clone()));
        let money2 = Arc::new(Mutex::new(money_tree[1].clone()));
        // let mut handles = vec![];
        // let empty: [(i32, u32, f64); 2] = [(1, 1, 1.0), (1, 1, 1.0)];
        // let e1: (i32, u32, f64) = (1, 1, 1.0);
        // let e2: (i32, u32, f64) = (1, 1, 1.0);
        thread::scope(|s| {
            let probability = Arc::clone(&prob1);
            let money = Arc::clone(&money1);
            let thread1 = s.spawn(move || {
                let prob = probability.lock().unwrap();
                let mon = money.lock().unwrap();
                simulate(
                    method[0],
                    number_of_runs[0],
                    starting_point[0],
                    prob.to_vec(),
                    mon.to_vec(),
                    falsecap[0],
                )
            });
            let probability = Arc::clone(&prob2);
            let money = Arc::clone(&money2);
            let thread2 = s.spawn(move || {
                let prob = probability.lock().unwrap();
                let mon = money.lock().unwrap();
                simulate(
                    method[1],
                    number_of_runs[1],
                    starting_point[1],
                    prob.to_vec(),
                    mon.to_vec(),
                    falsecap[1],
                )
                // println!("simulation 2 {} attempts at {}",e2.1, e2.2 );
                // println!("Final:{:?}", empty);
            });
            [thread1.join().unwrap(), thread2.join().unwrap()]
        })
    }

}

fn main() {

    //file input
    let mut file = File::open("./output.json").unwrap();
    let mut buff = String::new();
    file.read_to_string(&mut buff).unwrap();

    let data: Entry = serde_json::from_str(&buff).unwrap();
    let method_input = [data.simulation1.method, data.simulation2.method];
    let runs_input = [data.simulation1.runs, data.simulation2.runs];
    let start_input = [
        data.simulation1.starting_point,
        data.simulation2.starting_point,
    ];
    let probs_input = [
        data.simulation1
            .probability
            .iter()
            .map(|s| s as &str)
            .collect(),
        data.simulation2
            .probability
            .iter()
            .map(|s| s as &str)
            .collect(),
    ];
    let moneytree_input = [
        (*data.simulation1.moneytree).to_vec(),
        (*data.simulation2.moneytree).to_vec(),
    ];
    let falsecap_input = [data.simulation1.falsecap, data.simulation2.falsecap];
    let mut trials = data.trials;
    let duration = Instant::now();
    if trials < 1000000 {
        for _i in 0..trials {
            let entries = trial::simulate_doublethread(
                method_input,
                runs_input,
                start_input,
                probs_input.clone(),
                moneytree_input.clone(),
                falsecap_input,
            );
            // dbg!(entries);
            // println!{"For simulation 1, {} spent to attempt a total of {} times", entries[0].2, entries[0].1};
            // println!{"For simulation 2, {} spent to attempt a total of {} times", entries[1].2, entries[1].1};
            println!(
                "{} {} {:.3} {} {} {:.3}",
                entries[0].0, entries[0].1, entries[0].2, entries[1].0, entries[1].1, entries[1].2
            )
        }
    } else {
        trials /= 8;
        std::thread::scope(|s| {
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread1 = s.spawn(move || {
                let probs = &probably;
                let moneyy = &money_;
                for _i in 0..trials {
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs.clone(),
                        moneyy.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            let probably = probs_input.clone();
            let money_ = moneytree_input.clone();
            let _thread2 = s.spawn(move || {
                for _i in 0..trials {
                    let probs2 = &probably;
                    let moneyy2 = &money_;
                    let entries = trial::simulate_doublethread(
                        method_input,
                        runs_input,
                        start_input,
                        probs2.clone(),
                        moneyy2.clone(),
                        falsecap_input,
                    );
                    println!(
                        "{} {} {:.3} {} {} {:.3}",
                        entries[0].0,
                        entries[0].1,
                        entries[0].2,
                        entries[1].0,
                        entries[1].1,
                        entries[1].2
                    )
                }
            });
            // [thread1.join().unwrap(), thread2.join().unwrap()]
        })
    }
    //parameters printed at end
    println!(
        "{} {} {} {} {} {}",
        method_input[0],
        runs_input[0],
        falsecap_input[0],
        method_input[1],
        runs_input[1],
        falsecap_input[1]
    ); // So we share as the last output string... method number - max number of runs - falsecap

    let timethink = duration.elapsed();
    let duration1 = timethink.as_secs();
    let extra_time_info = timethink.subsec_nanos();
    // let DUR = {export {time:duration1}};
    let dur = json!({
        "Time":duration1,
        "Extended Time Details":extra_time_info
    });

    fs::remove_file("duration.json").expect("File delete failed!");
    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .open("duration.json")
        .unwrap();
    write!(file, "{}", dur).unwrap();

}
