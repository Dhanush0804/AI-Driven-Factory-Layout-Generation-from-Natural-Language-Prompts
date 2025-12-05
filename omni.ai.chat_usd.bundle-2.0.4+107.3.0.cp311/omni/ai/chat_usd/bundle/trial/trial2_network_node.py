from lc_agent import NetworkNode
import carb
from .trial2_node import Trial2Node
from omni.ai.langchain.agent.usd_code import USDCodeInteractiveNetworkNode
from omni.ai.langchain.agent.usd_code import SceneInfoNetworkNode

# Simple in-memory session storage for demo (replace with real session/user storage in production)
TRIAL2_SESSION = {}

class Trial2NetworkNode(NetworkNode):

    """Trial2 Network Node for handling complex prompts that require multiple steps, multiple objects, or complex scene construction.
    It will decompose the prompt into a numbered list of simple, direct prompts and pass it on to the Code Agent to perform the task.
    It will then collect the output from the Code Agent and set it as the output for this node.
    It will then pass the output to the next node in the network.
    It will then pass the output to the next node in the network.
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
        carb.log_info("Trial2NetworkNode initialized")
        self.default_node = "Trial2Node"

        self.metadata["description"] = """Agent to convert complicated prompts into simple prompts and pass it on to the Code Agent to perform the task"""
        self.metadata["examples"] = [
            "Create 4 walls as boundary for a room, place a cube in the center of the room and place 4 different objects at the corners of the room",
            "Build a table with four legs and put a vase on top of it",
            "Arrange three spheres in a row, each with a different color",
            "Create a staircase with 5 steps leading up to a platform",
            "Place a chair next to a desk and put a book on the desk",
            "Make a pyramid of cubes with a total of 10 cubes",
            "Add a window to the left wall and a door to the right wall",
            "Put a lamp above the table and turn it on",
            "Create a scene with a car parked inside a garage",
            "Build a bridge over a river and place two trees on each side",
            "Arrange five cones in a circle around a central sphere",
            "Place a robot in the room and have it face the door",
            "Add a rug under the table and a painting on the wall",
            "Create a bookshelf with three shelves and put books on each shelf",
            "Set up a dining table with four chairs and plates on the table",
        ]
            

    async def on_begin_invoke_async(self, network):
        # No change needed here for two-step workflow
        pass

    async def on_post_invoke_async(self, network, node):
        user_id = 'default_user'  # Replace with real user/session id in production
        outputs = []
        current_prompt = self.inputs.content if hasattr(self.inputs, "content") else ""
        proceed_keywords = ["proceed", "start", "run", "execute"]
        # If the user message is a proceed command, execute stored steps
        if current_prompt.strip().lower() in proceed_keywords:
            steps = TRIAL2_SESSION.get(user_id)
            if not steps:
                self.outputs.content = "No steps to execute. Please provide a complex prompt first."
                return
            for step in steps:
                code_node = USDCodeInteractiveNetworkNode(question=step)
                self >> code_node
                network.add_node(code_node)
                carb.log_info(f"Executing code agent for step: {step}")
                with network:
                    await code_node.ainvoke({})
                if hasattr(code_node.outputs, "content"):
                    outputs.append(f"Step: {step}\nResult: {code_node.outputs.content}")
            self.outputs.content = "\n\n".join(outputs)
            # Clear session after execution
            TRIAL2_SESSION.pop(user_id, None)
            return
        # Otherwise, treat as a complex prompt: decompose and store steps
        decomposer_node = Trial2Node(question=current_prompt)
        self >> decomposer_node
        await decomposer_node.ainvoke({})
        # Try to split steps by semicolon or newline
        steps_raw = decomposer_node.outputs.content if hasattr(decomposer_node.outputs, "content") else ""
        # Try both semicolon and newline splitting
        if ";" in steps_raw:
            steps = [s.strip() for s in steps_raw.split(";") if s.strip()]
        else:
            steps = [s.strip() for s in steps_raw.split("\n") if s.strip()]
        if not steps:
            self.outputs.content = "No steps could be decomposed from the prompt."
            return
        # Store steps in session
        TRIAL2_SESSION[user_id] = steps
        # Return steps to user and prompt for proceed
        formatted = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        self.outputs.content = (
            f"Here are the decomposed steps:\n{formatted}\n\nType 'proceed' to execute these steps."
        )
