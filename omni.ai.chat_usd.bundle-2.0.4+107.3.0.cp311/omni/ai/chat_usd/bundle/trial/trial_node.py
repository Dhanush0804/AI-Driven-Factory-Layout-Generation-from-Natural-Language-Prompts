from lc_agent import RunnableNode   
import carb

from ..utils.chat_model_utils import sanitize_messages_with_expert_type

class TrialNode(RunnableNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        carb.log_info("TrialNode initialized")
     

    async def on_begin_invoke_async(self, network):
        # Look for a SceneInfoNetworkNode among parents
        scene_info = None
        for parent in network.parents:
            from omni.ai.langchain.agent.usd_code import SceneInfoNetworkNode
            if isinstance(parent, SceneInfoNetworkNode):
                scene_info = parent.outputs.content
                break
        # Store scene_info for use in _sanitize_messages_for_chat_model
        
        self._scene_info = scene_info if scene_info else "[No scene information available]"

    def _sanitize_messages_for_chat_model(self, messages, chat_model_name, chat_model):
        messages = super()._sanitize_messages_for_chat_model(messages, chat_model_name, chat_model)
        # Combine greeting and scene info
        greeting = "Hello! Here is the current scene information:\n"
        combined_message = f"{greeting}{getattr(self, '_scene_info', '[No scene information available]')}"
        # Replace the last message's content with the combined message
              # Set the content for the last message, handling both dict and object types
        if messages:
            msg = messages[-1]
            # For dict type
            if isinstance(msg, dict):
                msg["content"] = combined_message
                # Fallback: ensure message is never empty
                if not msg["content"] or not str(msg["content"]).strip():
                    msg["content"] = "Hello! [No scene information available]"
            # For object type (e.g., HumanMessage)
            elif hasattr(msg, "content"):
                msg.content = combined_message
                if not msg.content or not str(msg.content).strip():
                    msg.content = "Hello! [No scene information available]"
        return sanitize_messages_with_expert_type(messages, "code", rag_max_tokens=0, rag_top_k=0)