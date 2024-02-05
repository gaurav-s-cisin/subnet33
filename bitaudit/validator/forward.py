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

import bittensor as bt
import time

from bitaudit.protocol import Audit
from bitaudit.validator.reward import get_rewards
from bitaudit.utils.uids import get_random_uids

from bitaudit.validator.dataset import preprocess_json, download_dataset, generate_labels, generate_random_path

def read_contract_code(file_path):
    # Read the contract code file in local
    with open(file_path, 'rt') as f:
        contract_code = f.readlines()

    # Filter out empty lines
    contract_code = [line for line in contract_code if line.strip()!='']
    
    return ''.join(contract_code)

async def forward(self):
    """
    The forward function is called by the validator every time step.

    It is responsible for querying the network and scoring the responses.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    # TODO(developer): Define how the validator selects a miner to query, how often, etc.
    # get_random_uids is an example method, but you can replace it with your own.

    # miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

    # TODO: Implement validation dataset download from huggingface
    # Choose a random file from the dataset and read the content and its labels
    # smart_contract = """
    # contract Fomo {
    #     uint256 public airDropTracker_ = 0;
    #     function airdrop() private view returns(bool) {
    #         uint256 seed = uint256(keccak256(abi.encodePacked((block.timestamp) / now)));
    #         if(seed < airDropTracker_)
    #             return true;
    #         else
    #             return false;
    #     }
    # }
    #
    # contract Overflow_add {
    #     uint8 sellerBalance = 0;
    #     function add(uint8 value) returns (uint){
    #         sellerBalance += value;
    #         return sellerBalance;
    #     }
    # }
    #
    # contract Overflow {
    #     function add_overflow() returns (uint256 _overflow) {
    #         uint256 max = 2**256 - 1;
    #         return max + 1;
    #     }
    # }
    # """

    # Download dataset from huggingface.
    # download_dataset()

    # TODO: Read the random smart contract file from the dataset and send it as a query
    smart_contract_path, file_no = generate_random_path()
    smart_contract = read_contract_code(smart_contract_path)

    # We will genrate sample labels from the outoput.csv file number corresponding it smart_contract that we will pass as task.
    # print("########## CODE ##########")
    # print(smart_contract)
    labels = generate_labels(file_no)

    # Mock-up contract code content
    # smart_contract = 'Hello, Have some fun!'
    # Mock-up label
    # label = { "Overflow": "Reentrancy Vulnerability" }

    if self.step % self.config.neuron.query_steps > 0:
        return

    available_axon_count = len(self.metagraph.axons) - 1 #Exclude itself

    # Selects available miners randomly
    miner_selection_size = min(available_axon_count, self.config.neuron.sample_size)
    miner_uids = get_random_uids(self, k=miner_selection_size)

    # The dendrite client queries the network.
    # try:
    if miner_selection_size == 0:
        bt.logging.info("No available miners at the moment.")
        return

    bt.logging.info('Querying %d random miners at step %d'%(miner_selection_size, self.step))
    bt.logging.info('Recommended Response: %s'%str(labels))

    try:
        start_time = time.time()
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],

            # Construct a Vulnerability query. This simply contains a single string.
            synapse=Audit(smart_contract_input=smart_contract),

            # All responses have the deserialize function called on them before returning.
            # You are encouraged to define your own deserialization function.
            deserialize=True,
            timeout=self.config.neuron.timeout,
        )

        exec_time = time.time() - start_time
        bt.logging.info("Execution time: %s" % str(exec_time))

        # TODO: Implement Exception handling for null responses
        if responses == [''] or responses == [] or not responses:
            bt.logging.info("Null or empty responses received, exiting function")
            return

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received responses: {responses}")

        # TODO: Implement process time info acquiry
        # exec_time = self.dendrite.process_time
        # bt.logging.info("Execution time:%s"%str(exec_time))
    except Exception as e:
        bt.logging.error("Error handling queries from miner's side: %str" % str(e))

    # Preprocess the json data
    label = preprocess_json(labels)
    responses = [preprocess_json(response) for response in responses]

    # TODO(developer): Define how the validator scores responses.
    # Adjust the scores based on responses from miners.
    rewards = get_rewards(self, label=label, responses=responses, response_time=exec_time)

    bt.logging.info(f"Scored responses: {rewards}")
    # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
    self.update_scores(rewards, miner_uids)
