"""
Use this script to control the env with your keyboard.
For this script to work, you need to have the PyGame window in focus.

See/modify `char_to_action` to set the key-to-action mapping.
"""
import sys
import gym

import numpy as np
from multiworld.envs.mujoco.sawyer_xyz.sawyer_door_hook import SawyerDoorHookEnv

from multiworld.envs.mujoco.sawyer_xyz.sawyer_pick_and_place import \
    SawyerPickAndPlaceEnv
# from multiworld.envs.mujoco.sawyer_xyz.sawyer_push_and_reach_env import \
#     SawyerPushAndReachXYEnv, SawyerPushAndReachXYZEnv
from multiworld.envs.mujoco.sawyer_xyz.sawyer_push_nips import SawyerPushAndReachXYEnv
from multiworld.envs.mujoco.sawyer_xyz.sawyer_push_and_reach_env_two_pucks import (
    SawyerPushAndReachXYDoublePuckEnv,
    SawyerPushAndReachXYZDoublePuckEnv,
)

import pygame
from pygame.locals import QUIT, KEYDOWN

from multiworld.envs.mujoco.sawyer_xyz.sawyer_reach import SawyerReachXYEnv, \
    SawyerReachXYZEnv

from multiworld.envs.mujoco.pointmass.pointmass import PointmassEnv

pygame.init()
screen = pygame.display.set_mode((400, 300))


char_to_action = {
    'w': np.array([0, -1, 0, 0]),
    'a': np.array([1, 0, 0, 0]),
    's': np.array([0, 1, 0, 0]),
    'd': np.array([-1, 0, 0, 0]),
    'q': np.array([1, -1, 0, 0]),
    'e': np.array([-1, -1, 0, 0]),
    'z': np.array([1, 1, 0, 0]),
    'c': np.array([-1, 1, 0, 0]),
    'k': np.array([0, 0, 1, 0]),
    'j': np.array([0, 0, -1, 0]),
    'h': 'close',
    'l': 'open',
    'x': 'toggle',
    'r': 'reset',
    'p': 'put obj in hand',
}


import gym
import multiworld
import pygame
# env_kwargs = dict(
#     sample_realistic_goals=True,
#     hand_low=(-0.20, 0.50),
#     hand_high=(0.20, 0.70),
#     puck_low=(-0.20, 0.50),
#     puck_high=(0.20, 0.70),
#     fix_reset=0.075,
#     heavy_puck=False,  # [True, False],
#     wall=True,
#     action_scale=0.02,
#     reward_type='vectorized_state_distance'
# )
# env = SawyerPushAndReachXYEnv(**env_kwargs)
# env = gym.make("SawyerPushAndReachArenaTestEnvBig-v0")

# env_kwargs = dict(
#     frame_skip=100,
#     action_scale=0.3,
#     ball_low=(-2, -0.5),
#     ball_high=(2, 1),
#     goal_low=(-4, 2),
#     goal_high=(4, 4),
#     model_path='pointmass_u_wall_big.xml',
# )
# env = PointmassEnv(**env_kwargs)

from multiworld.envs.mujoco.sawyer_xyz.sawyer_pick_and_place import SawyerPickAndPlaceEnvYZ
env_kwargs = dict(
    hand_low=(0.0, 0.43, 0.05), #(0.0, 0.43, 0.05), #(-0.1, 0.43, 0.02),
    hand_high=(0.0, 0.77, 0.20), #(0.0, 0.77, 0.2), #(0.0, 0.77, 0.2),
    action_scale=.02, #.02
    hide_goal_markers=True,
    num_goals_presampled=10,
    two_obj=False, #True
    structure=None, #None
    reset_p=(1.0, 0.0),
    goal_p=(0.0, 1.0),
)
env = SawyerPickAndPlaceEnvYZ(**env_kwargs)

NDIM = env.action_space.low.size
lock_action = False
obs = env.reset()
action = np.zeros(10)
gripped_closed = False
while True:
    done = False
    if not lock_action:
        action[:3] = 0
    for event in pygame.event.get():
        event_happened = True
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            char = event.dict['key']
            new_action = char_to_action.get(chr(char), None)
            if new_action == 'toggle':
                lock_action = not lock_action
            elif new_action == 'reset':
                done = True
            elif new_action == 'close':
                gripped_closed = True
            elif new_action == 'open':
                gripped_closed = False
            elif new_action == 'put obj in hand':
                print("putting obj in hand")
                env.put_obj_in_hand()
                action[3] = 1
            elif new_action is not None:
                action[:3] = new_action[:3]
            else:
                action = np.zeros(3)

            if gripped_closed:
                action[2] = 1
                # action[2] = 1
            else:
                action[2] = -1

                    # if closed_gripper:
            env.step(action[:len(env.action_space.low)])
    if done:
        obs = env.reset()
    env.render()
