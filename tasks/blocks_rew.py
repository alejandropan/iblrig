"@alejandro April 2019  -  Code for biased reward blocks.  Block reward probabilities are hard coded here"
########################## REWARD BLOCKS ######################################
import misc
import numpy as np


def get_block_len(factor, min_, max_):
    return int(misc.texp(factor=factor, min_=min_, max_=max_))


def update_block_params(tph):
    tph.block_rew_trial_num += 1
    if tph.block_rew_trial_num > tph.block_rew_len:
        tph.block_rew_num += 1
        tph.block_rew_trial_num = 1
        tph.block_rew_len = get_block_len(
            factor=tph.block_rew_len_factor, min_=tph.block_rew_len_min,
            max_=tph.block_rew_len_max)
        if tph.block_trial_num != 1 and tph.rew_probability_left == 0.4:
            tph.rew_probability_left = 0.8
        elif tph.block_trial_num != 1 and tph.rew_probability_left == 0.8:
            tph.rew_probability_left = 0.4
    return tph


def update_probability_left(tph):
    if tph.block_trial_num != 1:
        return tph.rew_probability_left
    if tph.block_num == 1 and tph.block_init_5050:
        return 0.5
    elif tph.block_num == 1 and not tph.block_init_5050:
        return np.random.choice(tph.rew_prob_set)
    #if tph.block_trial_num != 1:
     #   return tph.rew_probability_left #Need to check this line 
    elif tph.block_num == 2:
        return np.random.choice(tph.rew_prob_set)
    elif tph.rew_probability_left == 0.4:
        return 0.8
    elif tph.rew_probability_left == 0.8:
        return 0.4
###############################################################################
############ !!!!This is they key section for reward selection!!!!! ###########
###############################################################################

def draw_reward(position,rew_set, rew_probability_left):
    if position < 0 and rew_probability_left == 0.4:
        return int(np.random.choice(rew_set, p=[0.4, 0.6]))
    if position > 0 and rew_probability_left == 0.4:
        return int(np.random.choice(rew_set, p=[0.8, 0.2]))
    if position < 0 and rew_probability_left == 0.8:
        return int(np.random.choice(rew_set, p=[0.8, 0.2]))
    if position > 0 and rew_probability_left == 0.8:
        return int(np.random.choice(rew_set, p=[0.4, 0.6]))
    if position > 0 and rew_probability_left == 0.5:
        return int(1)
    if position < 0 and rew_probability_left == 0.5:
        return int(1)
        

###############################################################################
#I am macking unbiased position dependent on the proabbility of the rewarded 
#block if 80% on left trials, make it 80/2 instead 40  -  rew_probability_right
# is currently never declared is dependent in rew_probability_left  
###############################################################################
def init_block_len(tph):
    if tph.block_init_5050:
        return 90
    else:
        return get_block_len(
            factor=tph.block_rew_len_factor, min_=tph.block_rew_len_min,
            max_=tph.block_rew_len_max)


def init_rew_probability_left(tph):
    if tph.block_init_5050:
        return 0.5
    else:
        return np.random.choice(tph.block_rew_probability_set)