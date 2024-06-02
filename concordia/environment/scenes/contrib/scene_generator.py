# Copyright 2023 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from collections.abc import Sequence
import datetime

from concordia.associative_memory import formative_memories
from concordia.language_model import language_model
from concordia.typing.scene import SceneTypeSpec, SceneSpec


class SceneGenerator:
    """Class to generate scene specifications based on given parameters."""

    @staticmethod
    def generate_scene_spec(
        model: language_model.LanguageModel,
        scene_type_name: str,
        situation: str,
        length: int,
        start_time: datetime.datetime,
        participant_configs: Sequence[formative_memories.AgentConfig],
        num_rounds: int,
    ) -> SceneSpec:
        """Generate a complete scene specification.

        Args:
          model: A generative model for text generation.
          premise_name: The name to assign to the scene type.
          situation: The basis of the scene's premise, defaults if None.
          length: Desired length of the premise in words.
          start_time: When the scene starts.
          participant_configs: Configurations for participants in the scene.
          num_rounds: Number of rounds the scene should last.

        Returns:
          A SceneSpec object configured with the generated premise and other parameters.
        """

        if not situation:
            situation = "a random situation that a human might encounter in daily life"

        # Generate the premise text
        prompt = (
            f"Generate a scene where {situation} is the basis of the scene. The scene "
            f"should be {length} words long. Include details about objects, challenges, "
            "opportunities, and characters in the scene, written in the present tense. "
            "Write in a way that the characters in an agent based model can respond to "
            "the situation. Do not include instructions or a title in the output."
        )
        generated_premise = model.sample_text(prompt, max_characters=3500, max_tokens=3500)

        # Create the scene type specification
        scene_type_spec = SceneTypeSpec(
            name=scene_type_name,
            premise={pc.name: [generated_premise] for pc in participant_configs},
            conclusion=None,  # Optionally define a conclusion or other attributes
            action_spec=None,  # Optionally define action spec
            override_game_master=None,  # Optionally define a custom game master
        )

        # Return the complete scene specification
        return SceneSpec(
            scene_type=scene_type_spec,
            start_time=start_time,
            participant_configs=participant_configs,
            num_rounds=num_rounds,
        )
