import numpy as np 
from matplotlib import pyplot as plt

# Set a random seed
np.random.seed(0)

# Initialize an environment

# Each user is a context
# Each user is denoted by his/her index (ex: user 0 or user 3)
num_users = 5 

# Each advertisment is an action
num_ads = 10 # There are 10 ads 

# reward_table is a dictionary of key: the index of a user / value: np.array of the deterministic reward of each action (ad)
reward_table = {user: np.random.choice(10, size=num_ads) for user in range(num_users)}

# Implement IPS 
class IPS:
    def __init__(self):
        self.estimates = list()

    def get_estimate(self):
        """
        Append the IPS estimate of a single sample to self.estimates.
        You should implement this function
        """

    def evaluation(self, num_samples):
        """
        Get the mean of num_samples number of IPS estimates
        """
        return np.mean(self.estimates[:num_samples])

# Three policies    
class UniformlyRandom:
    def __init__(self, num_actions):
        """
        num_actions: number of actions (in this demo, it is equal to the number of ads)
        """
        self.num_actions = num_actions 

    def choose_action(self, context):
        """
        return a chosen action and action-probabilities
        """
        return np.random.choice(self.num_actions), [1 / self.num_actions] * self.num_actions

    def update(self, cb_sample):
        """
        UniformlyRandom is a stateless policy, which means it does not update itself
        based on the past rewards revelaed by it.

        (parameters)
        cb_sample: a tuple of (context, chosen action, reward revealed)
        """
        pass

class EpsilonGreedy:
    def __init__(self, num_actions, num_contexts, epsilon=0.1):
        """
        This is a CB verision of epsilon greedy

        (parameters)
        num_actions: number of actions (= number of ads)
        num_contexts: number of contexts (= number of users)
        epsilon: this policy chooeses a random action with epsilon probability 

        (Stored values)
        self.num_actions = num_actions 
        self.num_contexts = num_contexts
        self.num_actions_chosen: keep track of how many times each action is chosen for each context
        self.sum_rewards: keep track of the total reward of each action for each context

        The reason why self.num_actions_chosen is initialized with np.ones instead of np.zeros is
        to prevent division by zero in the function choose_action (line 68) 
        when an action has never been chosen so far for a given context.
        """
        self.num_actions = num_actions 
        self.num_contexts = num_contexts
        self.num_actions_chosen = {context: np.ones(num_actions) for context in range(num_contexts)}
        self.sum_rewards = {context: np.zeros(num_actions) for context in range(num_contexts)}
        self.epsilon = epsilon

    def choose_action(self, context):
        """
        return a chosen action and its probability
        """
        # Check which action is the best action 
        # The best action is the action that has the highest total reward for a given context
        best_action = np.argmax(self.sum_rewards[context] / self.num_actions_chosen[context])

        # Get action probabilities based on the best action
        # there is a (epsilon + epsilon/num_actions) probability of choosing the best action.
        # there is a (epsilon/num_actions) probability of choosing any other action
        action_probabilities = [self.epsilon / self.num_actions] * self.num_actions
        action_probabilities[best_action] += 1 - self.epsilon

        # Sample an action
        chosen_action = np.random.choice(self.num_actions, p=action_probabilities)

        # Record the number of times the chosen action is chosen
        self.num_actions_chosen[context][chosen_action] += 1

        return chosen_action, action_probabilities

    def update(self, cb_sample):
        """
        EpsilonGreedy is a stateful policy, which means it does update itself
        based on the past rewards revelaed by it.
        Thus, update function is necessary.

        (parameters)
        cb_sample: a tuple of (context, chosen action, reward revealed)
        """
        context, chosen_action, reward_revealed = cb_sample

        self.sum_rewards[context][chosen_action] += reward_revealed

# Implement your own simple stochastic policy (This should be different form the uniformly random policy)
class StochasticPolicy:
    def __init__(self):
        pass

    def choose_action(self, context):
        pass

    def update(self, cb_sample):
        pass

# Implement your own simple deterministic policy
class DeterministicPolicy:
    def __init__(self):
        pass

    def choose_action(self, context):
        pass

    def update(self, cb_sample):
        pass

# Initialize policies
epsilon = 0.1 # epsilon is a tunable parameter

uni_ran = UniformlyRandom(num_ads)
eps_greedy = EpsilonGreedy(num_ads, num_users, epsilon=epsilon)

# Start the demo
num_samples = 1000000 # total number of samples. Feel free to change this if you want to
new_policy_true_rewards = list() # Keep track of true rewards revealed by the new policy

# Implement the demo as specified by the comments below
old_policy = eps_greedy 
new_policy = uni_ran
ips_estimator = IPS()

for sample_index in range(num_samples): 
    # Context (user) revealed
    user = np.random.choice(num_users)

    # The old policy chooses an action
    old_chosen_action, old_probabilities = old_policy.choose_action(user)

    # The reward of the action chosen by the old policy is revealed
    reward = reward_table[user][old_chosen_action]

    # The new policy chooses an action
    new_chosen_action, new_probabilities = new_policy.choose_action(user)

    # Record the reward revealed by the new policy to get the true performance of the new policy
    new_policy_true_rewards.append(reward_table[user][new_chosen_action])

    # Store the CB sample in trace for evaluation
    ips_estimator.get_estimate("Implement")

    # Update the old policy if needed
    old_policy.update((user, old_chosen_action, reward))



# The expected value of the reward revealed by the new policy
# Actually, this is not the "true" expected value but a value 
# calculated by monte carlo methods.
# If you really want to be accurate, you can directly calculate 
# the true expected value using the environment defined at the beginning.
true_performance = np.mean(new_policy_true_rewards)

# Now you have the list of every IPS estimate you have got in self.estimates of ips_estimator.
# Use the list to solve the problems.
