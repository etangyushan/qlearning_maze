import random

class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # Set Parameters of the Learning Robot
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0

        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        Reset the robot
        """
        self.state = self.sense_state()
        # print ('self.state', self.state)
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
        Determine whether the robot is learning its q table, or
        exceuting the testing procedure.
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        Some of the paramters of the q learning robot can be altered,
        update these parameters when necessary.
        """
        if self.testing:
            # TODO 1. No random choice when testing
            self.epsilon = epsilon0
        else:
            # TODO 2. Update parameters when learning
            self.epsilon = random.random()

        return self.epsilon

    def sense_state(self):
        """
        Get the current state of the robot. In this
        """
        # TODO 3. Return robot's current state
        reward = self.maze.reward
        reversal_reward = {v:k for k,v in reward.items()}
        if self.action == None:
            return 'default'
        else:
            return reversal_reward[self.maze.move_robot(self.action)]
        
    def get_reward_bydirection(self, direction):
        """
        get reward by direction
        """
        # Random choose action due to action unstability
        oldloc = self.maze.robot['loc']
        reward = self.maze.move_robot(direction)
        self.maze.robot['loc'] = oldloc
        
        return reward
    
    def create_Qtable_line(self, state):
        """
        Create the qtable with the current state
        """
        # TODO 4. Create qtable with current state
        # Our qtable should be a two level dict,
        # Qtable[state] ={'u':xx, 'd':xx, ...}
        # If Qtable[state] already exits, then do
        # not change it.
        u_reward = self.get_reward_bydirection('u')
        d_reward = self.get_reward_bydirection('d')
        r_reward = self.get_reward_bydirection('r')
        l_reward = self.get_reward_bydirection('l')
        self.Qtable[state] = {'u':u_reward, 'd':d_reward, 'r':r_reward, 'l':l_reward}

    def get_maxreward_action(self, actions_reward):
        # print ("actions_reward:", actions_reward)
        action = max(actions_reward, key=lambda x:actions_reward.get(x))
        return actions_reward[action]

    def choose_action(self):
        """
        Return an action according to given rules
        """
        def is_random_exploration():

            # TODO 5. Return whether do random choice
            # hint: generate a random number, and compare
            # it with epsilon
            randomprob = random.random()
            if randomprob < self.epsilon:
                return True
            else:
                return False

        actions = self.maze.direction_bit_map
        # test = random.choice(self.maze.valid_actions)
        randomkey = random.randint(0, 3)
        # print ('actions:', actions)
        # print ('randomkey:', randomkey)
        if self.learning:
            if is_random_exploration():
                # TODO 6. Return random choose aciton
                return self.valid_actions[randomkey]
            else:
                # TODO 7. Return action with highest q value
                return max(actions, key=lambda x:actions.get(x))
        elif self.testing:
            # TODO 7. choose action with highest q value
            return max(actions, key=lambda x:actions.get(x))
        else:
            # TODO 6. Return random choose aciton
            return self.valid_actions[randomkey]

    def update_Qtable(self, r, action, next_state):
        """
        Update the qtable according to the given rule.
        """
        if self.learning:
            # TODO 8. When learning, update the q table according
            # to the given rules
            qvalue_state = self.Qtable[self.state][action]
            # print ("qvalue_state:", qvalue_state)
            maxqvalue_nextstate = self.get_maxreward_action(self.Qtable[next_state])
            # print ("maxqvalue_nextstate:", maxqvalue_nextstate)
            # print ("self.alpha:",self.alpha)
            # print ("self.gamma:",self.gamma)
            self.Qtable[self.state][action] = (1-self.alpha)*qvalue_state + self.alpha*(r +  self.gamma * maxqvalue_nextstate)
            
    def update(self):
        """
        Describle the procedure what to do when update the robot.
        Called every time in every epoch in training or testing.
        Return current action and reward.
        """
        self.state = self.sense_state() # Get the current state
        self.create_Qtable_line(self.state) # For the state, create q table line

        action = self.choose_action() # choose action for this state
        reward = self.maze.move_robot(action) # move robot for given action

        next_state = self.sense_state() # get next state
        self.create_Qtable_line(next_state) # create q table line for next state

        if self.learning and not self.testing:
            # print ("reward:", reward)
            # print ("action:", action)
            # print ("next_state:", next_state)
            self.update_Qtable(reward, action, next_state) # update q table
            self.update_parameter() # update parameters

        return action, reward


from Maze import Maze
mymaze = Maze(maze_size=(8, 11), trap_number = 3)

robot = Robot(mymaze)
robot.set_status(learning=True,testing=False)
print("test1:",robot.update())

print ("test2:",robot.Qtable)