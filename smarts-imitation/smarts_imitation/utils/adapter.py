from smarts_imitation.utils import common
import gym


def get_observation_adapter(mode="LANE"):
    # look_ahead = 10
    closest_neighbor_num = 6
    img_resolution = 40
    observe_lane_num = 3
    if mode == "GAIL":
        subscribed_features = dict(
            ego_pos=(2,),
            heading=(1,),
            speed=(1,),
            neighbor=(closest_neighbor_num * 4,),  # dist, speed, ttc
        )
    elif mode == "MADPO":
        subscribed_features = dict(
            ego_pos=(2,),
            heading=(1,),
            speed=(1,),
            neighbor=(closest_neighbor_num * 4,),  # dist, speed, ttc
            neighbor_dict=(closest_neighbor_num,),
        )
    elif mode == "LANE":
        subscribed_features = dict(
            ego_pos=(2,),
            heading=(1,),
            speed=(1,),
            neighbor_with_lanes=(closest_neighbor_num * 4,),  # dist, speed, ttc
        )
    else:
        raise NotImplementedError

    observation_space = gym.spaces.Dict(
        common.subscribe_features(**subscribed_features)
    )

    observation_adapter = common.get_observation_adapter(
        observation_space,
        observe_lane_num=observe_lane_num,
        resize=(img_resolution, img_resolution),
        closest_neighbor_num=closest_neighbor_num,
    )

    return observation_adapter


# def get_action_adapter():
#     def action_adapter(model_action):
#         assert len(model_action) == 2
#         throttle = np.clip(model_action[0], 0, 1)
#         brake = np.abs(np.clip(model_action[0], -1, 0))
#         return np.asarray([throttle, brake, model_action[1]])
#     return action_adapter


def get_action_adapter():
    def action_adapter(model_action):
        assert len(model_action) == 2
        return (model_action[0], model_action[1])

    return action_adapter
