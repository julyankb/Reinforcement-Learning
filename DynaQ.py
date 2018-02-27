import numpy as np
import matplotlib.pyplot as plt
import random
import blocking_shortcut_mazes as mazes
import animations
import sys

# Map observation to set of coordinates
def obs_to_state(obs):
  arr = np.array(obs.layers['P'], dtype=np.float)
  agent_position = np.argwhere(arr)[0]
  a,b = agent_position[0], agent_position[1]
  return a,b

def run_episode(game, switchpoint, q_table, model, cumulative_rewards, dynaplus, total_timesteps, hypers=(0.2,0.2,10)):
  eps, alpha, n = hypers[0], hypers[1], hypers[2]  

  steps_taken = 0
  reward_acheived = 0
  
  # Will keep a list of actions
  action_list = []
  
  # Init game
  obs, reward, gamma = game.its_showtime()
  
  # Init position memory
  last_pos = obs_to_state(obs)
  
  while True:
    # Get current state and select and action.
    a,b = obs_to_state(obs)
    
    # With probability epsilon
    if np.random.uniform(0,1) < eps:
      
      if dynaplus:
        # Dyna-Q+
        unexplored_actions = []
        explored_actions = []
        for action in (0,1,2,3):
          try:
            endpoint = model[a][b][action]
            explored_actions.append(action)
          except:
            unexplored_actions.append(action)
        
        if len(explored_actions) == 4 or len(unexplored_actions) == 4:
          action = np.random.randint(0,4)
          
        else:
          random_explored = np.random.choice(explored_actions)
          random_unexplored = np.random.choice(unexplored_actions)
          action = np.random.choice((random_explored, random_unexplored), p=(0.75, 0.25))
      
      else:
        action = np.random.randint(0,4)
    
    # Otherwise
    else:
      action = np.argmax(q_table[a][b])
   
    # Action results in a reward and subsequent state.
    obs, reward, gamma = game.play(action)
    a_,b_ = obs_to_state(obs)
   
    
    # Keep a list of actions taken.
    current_pos = (a_,b_)
    #print(current_pos, last_pos)
    if current_pos != last_pos:
      action_list.append(action)
      last_pos = current_pos
    else:
      action_list.append(-1)
      last_pos = current_pos
    

    # Update model with visited position.
    '''
    Each visited poisition has 4 possible actions, each of which have
    a next state and a resulting reward. 
    '''
    model[(a,b)] = {}
    model[(a,b)][action] = ((a_,b_), reward)

    # Update Q-table.
    q_table[a][b][action] += alpha * (reward + gamma * np.max(q_table[a_][b_]) 
                                      - q_table[a][b][action])

    # Update reward achieved.
    #reward_acheived += reward

    # Update cumulative reward.
    cumulative_rewards.append(cumulative_rewards[-1] + reward)
    
    # Increment time steps.
    steps_taken += 1
    
    
    # ** Temp code, not sure if should break here.
    if total_timesteps + steps_taken == switchpoint:
        action_list.append(-3)
        break
	
    # End episode if player is on target 'G'.
    if gamma == 0:
      action_list.append(-2)
      break

    # If player not on G. Imagine scenarios based on memory, update Q table. 
    # Remember what you've done and what resulted from it, 
    # then reinforce that without taking any actions.
    for i in range(n):
      state = random.choice(list(model.keys()))
      action = np.random.choice(list(model[state].keys()))
      next_state, reward = model[state][action][0], model[state][action][1]

      a,b = state
      a_,b_ = next_state
      q_table[a][b][action] += alpha * (reward + gamma * np.max(q_table[a_][b_]) 
                                        - q_table[a][b][action])

  return q_table, model, cumulative_rewards, steps_taken, action_list
# =========================================================================


def DynaQ(game_name='blocking_maze', n_episodes = 100, eps = 0.2, alpha = 0.2, n = 10, dynaplus=0):
  
  switchpoint = 1000 if game_name == 'blocking_maze' else 3000

  q_table = np.zeros((8,11,4))
  model = {}

  time_steps = 0
  action_lists = []
  cumulative_rewards = [0]
  for episode in range(n_episodes):
    if time_steps >= switchpoint:
    
      if game_name == 'blocking_maze':
        game = mazes.make_blocking_maze(blocked=True)
      elif game_name == 'shortcut_maze':
        game = mazes.make_shortcut_maze(shortcut=True)
  
    else:
      if game_name == 'blocking_maze':
        game = mazes.make_blocking_maze(blocked=False)
      elif game_name == 'shortcut_maze':
        game = mazes.make_shortcut_maze(shortcut=False)
    
    # Run one episode of Dyna-Q
    q_table, model, cumulative_rewards, steps_taken, action_list = run_episode(game, 
								switchpoint, # Must include switchpoint
								# 1) break if reach switch point
								# 2) know if blocking or shortcut
								q_table, 
								model, 
								cumulative_rewards, 
								dynaplus = dynaplus,
								total_timesteps=time_steps, 
								hypers=(eps, alpha, n))
  
    action_lists.append(action_list)
    time_steps += steps_taken
  
  return cumulative_rewards, action_lists

# ============================================================================
def plot_avg_cumulative_rewards(num_layers, game_name = 'blocking_maze'):
  
  dyna_layers = []
  dynaplus_layers = []
  
  for dynaplus in [0,1]:
    n_episodes = 100 if game_name=='blocking_maze' else 300
    blocking_maze = 1
    shortcut_maze = 0
    switchpoint = 1000 if game_name == 'blocking_maze' else 3000

    for i in range(num_layers):
      cumulative_rewards = [0]
      q_table = np.zeros((8,11,4))
      model = {}
      cumulative_rewards = [0]

      total_timesteps = 0
      for episode in range(n_episodes):
        if total_timesteps >= switchpoint:
          if game_name == 'blocking_maze':
            game = mazes.make_blocking_maze(blocked=True)
          elif game_name == 'shortcut_maze':
            game = mazes.make_shortcut_maze(shortcut=True)
        else:
          if game_name == 'blocking_maze':
            game = mazes.make_blocking_maze(blocked=False)
          elif game_name == 'shortcut_maze':
            game = mazes.make_shortcut_maze(shortcut=False)

        # Run one episode of Dyna-Q
        q_table, model, cumulative_rewards, steps_taken, action_list = run_episode(game, switchpoint, q_table, model, cumulative_rewards, dynaplus, total_timesteps=total_timesteps, hypers=(0.2,0.2,10))

        total_timesteps += steps_taken

      if dynaplus:
        dynaplus_layers.append(cumulative_rewards)
      else:
        dyna_layers.append(cumulative_rewards)
  
  cumulative_rewards_dyna, cumulative_rewards_dynaplus = [sum(e)/len(e) for e in zip(*dyna_layers)], [sum(e)/len(e) for e in zip(*dynaplus_layers)]
  plt.plot(cumulative_rewards_dyna, label='Dyna-Q')
  plt.plot(cumulative_rewards_dynaplus, label='Dyna-Q+')
  if game_name == 'blocking_maze':
    plt.axvline(1000, c='r', linestyle='--', linewidth=1)
  elif game_name == 'shortcut_maze':
    plt.axvline(3000, c='r', linestyle='--', linewidth=1)

  plt.title('Average cumulative reward - %s'%game_name, fontweight='bold')
  plt.xlabel('Time steps')
  plt.ylabel('Cumulative reward')
  plt.legend()
  #plt.savefig('avg_cumulative_rewards_%s.png'%game_name)
  plt.show()

# =============================================================================

def make_hyperparam_graph(game_name='blocking_maze', toy=False, save_output=0):
  if toy:
    # toy example
    eps_list = np.linspace(0.1, 0.9, 2)
    alpha_list = np.linspace(0.1,0.9, 2)
    n_list = [int(n) for n in np.linspace(0,10, 2)]
  else:
    eps_list = np.linspace(0.01, 0.99, 10)
    alpha_list = np.linspace(0.01,0.99, 10)
    n_list = [int(n) for n in np.linspace(0,200, 10)]

  hyperparam_combinations = []
  for eps in eps_list:
    for alpha in alpha_list:
      for n in n_list:
        hyperparam_combinations.append((eps,alpha,n))


  overall_steps = []
  print('eps, alpha, n')
  for i, hc in enumerate(hyperparam_combinations):
    print('Combination %s/%s -- %s'%(i, len(hyperparam_combinations), hc))
    cumulative_rewards, _ = DynaQ(game_name, 
				n_episodes=10, 
				eps=hc[0], 
				alpha=hc[1], 
				n=hc[2])
    overall_steps.append(len(cumulative_rewards))


  tuples = sorted(zip(overall_steps, hyperparam_combinations))
  overall_steps = [tup[0] for tup in tuples]
  hyper_sets = [ '%0.2f %0.2f %s'%(tup[1][0], tup[1][1], tup[1][2]) for tup in tuples ]
  
  plt.plot(overall_steps)
  #plt.xticks([i for i in range(len(overall_steps))], hyper_sets, rotation='vertical', fontsize=5)
  plt.title('Hyperparam. combinations (eps, alpha, n) \nvs. steps taken over 10 episodes')
  plt.xlabel('Hyperparameter combinations')
  plt.ylabel('Steps over 10 episodes')
  plt.tight_layout()
  if save_output:
    plt.savefig('hyperparams.png')
    with open('hyperparams.sorted', 'w') as outfile:
      outfile.write('eps alpha n steps\n')
      for hc, steps in zip(hyper_sets, overall_steps):
        outfile.write('%s %s\n'%(hc, steps))
  else:
    plt.show()

#plot_avg_cumulative_rewards(30, sys.argv[1])
