MAX_TOKEN_LENGTH = 16384
MODEL_NAME = "codellama/CodeLlama-13b-Instruct-hf"
MIN_STAKE = 100
PROMPT_TEMPLATE = """
You are an AI smart contract auditor.
You will be given a smart contract code. Review the given smart contract code and detect the smart contract vulnerabilities in it with their vulnerability categories. All vulnerabilities would be categorized into six classes: Block Numer Dependency, Integer Overflow, Reentrancy Vulnerability, Dangerous Delegatecall, Timestamp Dependency, and Unchecked External Call.
%s
Check the whole code and detect all vulnerabilities in it with their contract names and vulnerability categories they belong.
Do not include any explanations or variables, only contract names and vulnerability categories.
Return the response in the json type with contract names as keys and according vulnerability categores as values.
Response:
"""
HUGGINGFACE_TOKEN = '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'
HUGGINGFACE_REPO_ID = "SarthakG/smart_contract"
OPENAI_COMPLETIONS_MODEL = "gpt-3.5-turbo"
OPENAI_COMPLETIONS_MAX_TOKENS = 3000
OPENAI_COMPLETIONS_TEMPERATURE = 0
OPENAI_COMPLETIONS_API_KEY = ""
PROMPT_TEMPLATE_OPEN_AI = """
You are an AI smart contract auditor.
You will be given a smart contract code.
that code contains multiple contracts after the name contract.
Review the given smart contract code and detect the smart contract vulnerabilities in it with their vulnerability categories. 
All vulnerabilities would be categorized into six classes: 
- Block Numer Dependency
- Integer Overflow
- Reentrancy Vulnerability
- Dangerous Delegatecall
- Timestamp Dependency
- Unchecked External Call.

Remember that each contract will go under only one vulnerability categorie.
Do not change the name of the contract

Check the whole code and detect all vulnerabilities in it with their contract names and vulnerability categories they belong.
Do not include any explanations or variables, only contract names and vulnerability categories.
Return the response in the json type with contract names as keys and according vulnerability category as value.

Guideline:- 
    - Iterate through contract by contract into the provided smart_contract and check each contract against the given six
      vulnerability categories.
    - Do multiple check of contract against the categories and remember the correct contract name and vulnerability category 
      and put it in key value pairs in reponse json object.
    - Keep in mind that not all the contracts may have vulnerability hence skip those contracts and do not add those into
      final json response.
    - While cross refencing smart_contract against the vulnerability categories use best of your knowledge to thorougly check
      possible vulnerability category and present it in final json object.
    - if there is no vulnerability detected for any contract do not include that contract into final json object.
    - Only add contract when you are 200 % sure that it contrains any vulnerabilty.

only provide a RFC8259 compliant JSON response following this format without deviation.
Output format:-
    {
        "contract_name" : "vulnerability category"
        # As many contract name as you find vulnerability into it along with its category
    }
    -------------------------------------------
"""