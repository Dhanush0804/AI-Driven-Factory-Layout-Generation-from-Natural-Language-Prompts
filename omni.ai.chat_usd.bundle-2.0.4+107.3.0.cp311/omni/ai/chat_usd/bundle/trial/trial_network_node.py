from lc_agent import NetworkNode
import carb
from omni.ai.langchain.agent.usd_code import SceneInfoNetworkNode


class TrialNetworkNode(NetworkNode):

    """Trial Network Node for handling hello messages"""
    def __init__(self,scene_info=True, **kwargs):
        super().__init__(**kwargs)
        carb.log_info("TrialNetworkNode initialized")
        self.default_node = "TrialNode"

        self.metadata["description"] = """Agent to print Hello World when user says hello"""
        self.metadata["examples"] = [
            "Hello",
            "Hi",
        ]
     
    async def on_begin_invoke_async(self, network):
        # Chain SceneInfoNetworkNode to TrialNode
        question = (
            "IMPORTANT: ONLY return information for prims (such as cubes, cones, spheres, etc.) that are descendants of the Xform prim named 'World' (i.e., under the /World hierarchy) in the current scene.\n"
            "Include only prims under Xform prim named 'World'.\n"
            "Do NOT include any Xform prims, only mesh/shape prims.\n"
            "For each prim, print each parameter on a new line, in this exact format:\n"
            "Entity type: <type> (e.g., Cube, Cone, Sphere)\n"
            "Entity name: <name of the prim>\n"
            "Prim path: <prim path>\n"
            "bounding box: <bounding box values>\n"
            "position: <position values>\n"
            "scale: <scale values>\n"
            "rotation: <rotation values>\n"
            "Print a blank line between each entity.\n"
            "Repeat for each. Do NOT include any other information or prim types. Do NOT include world or local bounds. Do NOT include /Environment/ground.\n"
            "ONLY use the format below. Do NOT add any extra text or explanation.\n"
            "Example:\n"
            "Entity type: Cube\n"
            "Entity name: Cube_01\n"
            "Prim path: /World/Cube_01\n"
            "bounding box: [min: (0,0,0), max: (1,1,1)]\n"
            "position: (0.5, 0.5, 0.5)\n"
            "scale: (1, 1, 1)\n"
            "rotation: (0, 0, 0)\n"
            "\n"
            "Entity type: Cone\n"
            "Entity name: Cone_01\n"
            "Prim path: /World/SomeGroup/Cone_01\n"
            "bounding box: [min: (2,2,2), max: (3,3,3)]\n"
            "position: (2.5, 2.5, 2.5)\n"
            "scale: (1, 2, 1)\n"
            "rotation: (0, 90, 0)\n"
            "\n"
        )
        scene_info_node = SceneInfoNetworkNode(
            question=question,
            enable_interpreter_undo_stack=False,
            max_retries=1,
            enable_rag=False,
        )
        from .trial_node import TrialNode
        trial_node = TrialNode()
        self >> scene_info_node >> trial_node