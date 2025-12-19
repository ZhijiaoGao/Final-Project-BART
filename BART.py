from psychopy import visual, event, core, data, gui, sound
import random
#########
#Participant Info (ID+Demographics)
#########
exp_info = {
    'participant_id':' ',
    'age':' ',
    'gender': ['Male', 'Female', 'Non-binary', 'Prefer not to say']
}
dlg = gui.DlgFromDict(
    dictionary=exp_info,
    title='BART Experiment',
    order=['participant_id', 'age', 'gender']
)
if not dlg.OK:
    core.quit()
#########
#Experiment setup
#########
win = visual.Window([1920, 1080], color='white', units='pix')
balloon = visual.Circle(win, radius=40, fillColor='red', lineColor='red')
info_text = visual.TextStim(win, pos=(0,-350), color='black',height=35)
score_text = visual.TextStim(win, pos=(0, 350), color='black', height=35)
instruction_text = visual.TextStim(win, height=50, wrapWidth=1000, color='black')
explosion_text = visual.TextStim(win, text='BOOM!', height=70, color='red')
boom_sound = sound.Sound('pop.mp3')
#BART Parameters
n_practice_trial = 1
n_trials=30
reward_per_pump = 0.05
max_pumps=128
total_score=0
#Data handler
exp = data.ExperimentHandler(name='BART', extraInfo=exp_info, dataFileName=f"BART_{exp_info['participant_id']}" )
########
#Instructions
########
instructions = [
    "Welcome to the experiment!\n\n"
    "Once the experiment starts, you will see a balloon (a red round shaped object).\n\n"
    "If you wish to pump the balloon, press SPACE.\n"
    "Each pump earns money, but also increases the risk of explosion.\n\n"
    "Press SPACE to continue.",
    
    "At any time, you can press C to cash out.\n\n"
    "If you cash out, you keep the money earned for that balloon.\n"
    "If the balloon EXPLODES, you earn NOTHING for that balloon.\n\n"
    "Press SPACE to continue.",
    
    "Keep in mind: The balloon can explode at any pump.\n"
    "In other words, the risk of explosion increases as the balloon gets bigger.\n\n"
    "GOAL: Try to earn as much money as possible.\n\n"
    "Now, press SPACE to begin."
]

for page in instructions:
    instruction_text.text=page
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

##################################
# ATTENTION CHECK
##################################
attention_text = visual.TextStim(
    win,
    text=(
        "Attention Check:\n\n"
        "Which key allows you to cash out?\n\n"
        "A.  SPACE\n"
        "B.  C\n"
        "C.  ESC"
    ),
    wrapWidth=1000,
    color='black',
    height=50
)

attention_text.draw()
win.flip()
key = event.waitKeys(keyList=['a', 'b', 'c'])[0]
attention_correct=(key=='b')

feedback = visual.TextStim(
    win,
    text="Correct! Next, you will do a practice run." if attention_correct else
        "Incorrect. You should press C to cash out. Please pay close attention to the experiment. Now, let's move on to a practice run.",
    color='black',
    height=50
)
feedback.draw()
win.flip()
core.wait(3.5)

exp.addData('attention_check_correct', attention_correct)
exp.nextEntry()

#########################
#One Practice Trial
#########################
for trial in range(n_practice_trial):
    pumps=0
    trial_reward=0
    balloon.radius=40
    
    while True:
        balloon.draw()
        info_text.text="Practice Trial\nSpace=Pump    C=Cash Out"
        info_text.draw()
        score_text.text = f"Current:${trial_reward:.2f}"
        score_text.draw()
        win.flip()
        
        
        keys=event.waitKeys(keyList=['space','c'])
        
        
        if 'space' in keys:
            pumps += 1
            trial_reward += reward_per_pump
            balloon.radius += 3
            explosion_prob = 1/(max_pumps - pumps + 1)
            
            
            if random.random() < explosion_prob:
                boom_sound.play()
                explosion_text.draw()
                win.flip()
                core.wait(1)
                break
                
        if 'c' in keys:
            break
            


###########################################
#Transitioning to the main trials
###########################################
instruction_text.text=(
    "Congrats! You just finished the practice trial.\n\n"
    "The real trials will now begin!\n"
    "Your earnings will now start to count.\n\n"
    "Press SPACE to continue when you are ready."
)
instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])



##################################
# MAIN TRIALS BEGIN HOORAY
##################################
for trial in range(n_trials):
    pumps=0
    trial_reward=0
    balloon.radius=40
    exploded=False
    
    while True:
        balloon.draw()
        info_text.text="SPACE = Pump    C = Cash Out"
        info_text.draw()
        score_text.text=(
            f"Trial {trial+1}/{n_trials}\n"
            f"Current: ${trial_reward:.2f} | Total:${total_score:.2f}"
        )
        score_text.draw()
        win.flip()
        
        
        keys=event.waitKeys(keyList=['space','c','escape'])
        
        if 'escape' in keys:
            win.close()
            core.quit()
            
        if 'space' in keys:
            pumps += 1
            trial_reward += reward_per_pump
            balloon.radius += 3
            explosion_prob=1/(max_pumps - pumps +1)
        
            if random.random()<explosion_prob:
                exploded=True
                trial_reward=0
                boom_sound.play()
                explosion_text.draw()
                win.flip()
                core.wait(1)
                break
        
        if 'c' in keys:
            total_score += trial_reward
            break
            
        ##trial feedback##
    if exploded:
        feedback_msg=(
            f"Balloon Exploded!\n\n"
            f"Pumps:{pumps}\n"
            f"Trial Earnings: $0.00\n\n"
            f"Total Earnings: ${total_score:.2f}"
        )
    else:
        feedback_msg=(
            f"You cashed out!\n\n"
            f"Pumps:{pumps}\n"
            f"Trial earnings: ${trial_reward:.2f}\n\n"
            f"Total earnings: ${total_score:.2f}"
        )
        
    
    trial_feedback=visual.TextStim(win, text=feedback_msg, wrapWidth=1000, color='black', height=50)
    trial_feedback.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
        
        
        
    ####save data#####
        
    exp.addData('Trial', trial+1)
    exp.addData('Pumps', pumps)
    exp.addData('Exploded', exploded)
    exp.addData('Trial_Reward', trial_reward)
    exp.addData('Total_Score', total_score)
    exp.nextEntry()



####################
####Final Screen for Participants####
####################

final_text=visual.TextStim(
    win,
    text=(
        "Experiment Completed!\n\n"
        f"Your total earnings: ${total_score:.2f}\n\n"
        "Thank you for participating! Happy Holidays!\n\n"
        "Press SPACE to exit experiment. :)"
    ),
    wrapWidth=1000,
    color='black',
    height=50
)

final_text.draw()
win.flip()
event.waitKeys(keyList=['space'])


####################################
##Save & Quit##
####################################
exp.saveAsWideText(f"BART_{exp_info['participant_id']}.csv")
win.close()
core.quit()
        














    













