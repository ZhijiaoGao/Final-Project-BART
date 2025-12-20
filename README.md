# Final-Project-BART
Programming Course Final Project - BART

This repository contains a Python version of the **Balloon Analogue Risk Task (BART)** using **PsychoPy**.

The task is designed to measure **risk-taking behavior** by having participants to pump a balloon (to earn rewards) or to cash out, with each pump increasing the risk of balloon explosion.


------

## Experiment Overview

- For each trial, participants pump the balloon by pressing **SPACE**
- Each pump increases: 1) The balloon size 2) The potential reward 3) The risk of explosion
- For each trial, participants can press **C** to cash out at any time
- If the balloon explodes, participants earn **nothing** for that trial
- Total earnings accumulate across 30 trials

The flow of the experiment is:
1) Instruction screens
2) An attention check
3) 1 practice trial
4) 30 actual trials
5) Trial-by-trial feedback
6) Data saved in .csv and exit


------

## Installment Requirements

1) Download PsychoPy
2) Download the sound effect file **pop.mp3**
3) Make sure everything is in the same folder/location.
4) The output file should look like **BART_3.csv** (an example output file from me)
5) If you complete all trials and press space to exit in the end (meaning going through the full experiment), you will have two saved files (because there is a forced save in the end of the code) and the content should be the same. 

------

## Instruction to run the code

Download the code file **BART.py** and open it with PsychoPy. Again, make sure things are all in the same place. Feel free to contact me if any questions!

------
