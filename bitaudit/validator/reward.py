# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import torch
import json
from typing import List
import bittensor as bt


def reward(self, label: dict, response: dict, response_time) -> float:
    """
    Reward the miner response to the Audit request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """

    bt.logging.info("Response: %s" % str(response))
    bt.logging.info("Preferred Answer: %s" % str(label))

    tp_contracts = list(set(response.keys()) & set(label.keys()))
    fp_contracts = list(set(response.keys()) - set(label.keys()))
    fn_contracts = list(set(label.keys()) - set(response.keys()))

    # Vulnerability Detection Score
    # Should focus on Recall to reduce undetected vulnerabilities
    try:
        recall = float(len(tp_contracts) / (len(tp_contracts) + len(fn_contracts)))
    except:
        recall = 0

    # Need some penalty with precision cause one can predict all contracts as vulnerabilities
    try:
        precision = float(len(tp_contracts) / (len(tp_contracts) + len(fp_contracts)))
    except:
        precision = 0

    # Get the score with weighted sum of recall and precision
    # Should set more weights on recall, that is 1 > alpha > 0.5
    if self.config.neuron.recall_weight > 1:
        detect_score = recall
    elif self.config.neuron.recall_weight < 0:
        detect_score = precision
    else:
        detect_score = recall * self.config.neuron.recall_weight + precision * (1 - self.config.neuron.recall_weight)

    # Vulnerability Classification Score
    # Check if detected vulnerabilities are classified correctly
    # TODO: Double check this mechanism
    true_classifi = 0
    total_vuls = len(tp_contracts)
    if total_vuls > 0:
        try:
            for vul in tp_contracts:
                if response[vul] == label[vul]:
                    true_classifi += 1
        except:
            pass
        classifi_score = float(true_classifi / total_vuls)
    else:
        classifi_score = 1

    # Response time score
    response_time_score = max(1 - response_time / self.config.neuron.timeout, 0)

    # Weighted some of detection score, classification score, and response time score
    overall_score = detect_score * self.config.neuron.detect_score_weight + \
                    classifi_score * self.config.neuron.classifi_score_weight + \
                    response_time_score * (1 - self.config.neuron.detect_score_weight - self.config.neuron.classifi_score_weight)
    bt.logging.info(
        "Detection Score: %f | Classification Score: %f | Response Time Score: %f | Overall Score: %f"%
        (detect_score, classifi_score, response_time_score, overall_score)
    )

    return overall_score


def get_rewards(
    self,
    label: dict,
    responses: List[dict],
    response_time: float,
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - label (dict): The label of the query sent to the miner.
    - responses (List[dict]): A list of responses from the miner.

    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """
    # Get all the reward results by iteratively calling your reward() function.
    return torch.FloatTensor(
        [reward(self, label, response, response_time) for response in responses]
    ).to(self.device)
