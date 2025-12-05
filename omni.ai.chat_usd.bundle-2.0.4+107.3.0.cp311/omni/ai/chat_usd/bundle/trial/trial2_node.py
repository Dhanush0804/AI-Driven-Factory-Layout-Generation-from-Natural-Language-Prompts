from lc_agent import RunnableNode
import carb 

from ..utils.chat_model_utils import sanitize_messages_with_expert_type

class Trial2Node(RunnableNode):
    """
    Trial2Node: Decomposes complex scene-building prompts into simple, atomic steps.
    In the first step, only decompose and return the steps for user review.
    Execution of steps is only performed after explicit user confirmation (e.g., user types 'proceed').
    """

    def __init__(self,
                 enable_code_interpreter=True,
                 code_interpreter_hide_items=None,
                 enable_code_atlas=True,
                 enable_metafunctions=True,
                 enable_interpreter_undo_stack=True,
                 max_retries=1,
                 enable_code_promoting=True,
                  **kwargs):
        super().__init__(**kwargs)
        carb.log_info("Trial2Node initialized")

    def _sanitize_messages_for_chat_model(self, messages, chat_model_name, chat_model):
        messages = super()._sanitize_messages_for_chat_model(messages, chat_model_name, chat_model)

        # Add a system prompt to instruct the LLM to decompose the prompt ONLY (not execute)
        system_prompt = (
            "You are an expert at breaking down complex scene-building instructions into simple, atomic steps. "
            "Given a complex prompt, output a numbered list of simple, direct prompts, one per line, that can be executed by a code agent. "
            "Do NOT execute or describe the execution, only decompose and return the steps for user review. "
            "Wait for explicit user confirmation (such as 'proceed') before any execution is performed."
        )
        # Insert system prompt at the start
        if messages and isinstance(messages[0], dict):
            messages.insert(0, {"role": "system", "content": system_prompt})
        elif messages and hasattr(messages[0], "content"):
            messages.insert(0, type(messages[0])(content=system_prompt))
        return sanitize_messages_with_expert_type(messages, "code", rag_max_tokens=0, rag_top_k=0)