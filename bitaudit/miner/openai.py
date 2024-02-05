import os
import logging
import bittensor as bt
import bitaudit
from typing import Optional, Text
from openai import OpenAI
logger = logging.getLogger(__name__)


def get_text_completion(prompt: Text) -> Optional[Text]:
    logger.info(f"LLM prompt: \n{prompt}\n")

    client = OpenAI(
        api_key=os.environ.get("OPENAI_COMPLETIONS_API_KEY", None))
    completion = client.chat.completions.create(model=os.environ.get("OPENAI_COMPLETIONS_MODEL", "gpt-3.5-turbo"),
                                                temperature=int(os.environ.get("OPENAI_COMPLETIONS_TEMPERATURE", 0)),
                                                messages=[
                                                    {"role": "user",
                                                     "content": prompt}
                                                ],
                                                max_tokens=int(
                                                    os.environ.get("OPENAI_COMPLETIONS_MAX_TOKENS", 100)),
                                                )
    choices = completion.choices[0].message
    try:
        choice = choices.content
        logger.info(f"LLM response: \n{choice}\n")
        return choice
    except Exception as e:
        logger.exception(f"Error occurred while extracting the LLM response. {e}")
        return None


def validating_smart_contract_for_miner(self, synapse: bitaudit.protocol.Audit) -> str:
    """
    It is responsible for diagnosing vulnerability in given smart contract.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    # Get the file path of model
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
    # """
    smart_contract = synapse.smart_contract_input
    # TODO: Implemented openai auditing. Check this
    # response_data = get_text_completion(
    #     prompt=f'Identify the vulnerability, function name and generate explation from given below blockchain smart contract and label the Vulnerability category to genrated response from this list ["Block Number", "Dependency Dangerous", "Delegatecall Integer", "Overflow Reentrancy", "Timestamp Dependency", "Unchecked External Call"], if there are someother vulnerabilities so mention it. Format will be like - ["Function Name: ", "Vulnerability category: ", "Explanation: "], Also add recommnadation for fixation smart contract. Smart Contract - {smart_contract}')
    bt.logging.info(smart_contract)
    response_data = ''

    print(response_data)

    # # Instantiate Axon and Dendrite
    # axon = bittensor.axon
    # dendrite = bittensor.dendrite

    # # List of subnet miners and subnet validators
    # subnet_miners = ["miner1", "miner2", "miner3"]
    # subnet_validators = ["validator1", "validator2", "validator3"]

    # for miner in subnet_miners:
    #     try:
    #         for validator in subnet_validators:
    #             axon.send_message(
    #                 message=response_data,
    #                 receiver=validator,
    #                 amount=0,  # Adjust the amount of tokens to send if required
    #             )
    #         print(f"Response sent successfully from {miner} via Axon.")
    #     except Exception as e:
    #         pass
    #         # print(f"Error sending response from {miner} via Axon:", str(e))

    # # Receive responses via Dendrite on subnet validators' side
    # for validator in subnet_validators:
    #     try:
    #         received_message = dendrite.receive_message()
    #         print(f"Received message via Dendrite on {validator}:",
    #               received_message)
    #     except Exception as e:
    #         pass
    #         # print(f"Error receiving message via Dendrite on {validator}:", str(e))
    
    return response_data