from typing import List, Any
from llama_index.core.schema import TransformComponent, BaseNode



class MetadataExclusionSetter(TransformComponent):
    """
    A custom transformation to set metadata keys for exclusion from LLM and embedding.
    """
    model_config = {"extra": "allow"}

    def __init__(
        self,
        exclude_llm: List[str] = [],
        exclude_embed: List[str] = [],
        **kwargs: Any,
    ) -> None:
        """
        Initializes the MetadataExclusionSetter with lists of keys to exclude.

        Args:
            exclude_llm (List[str]): Metadata keys to exclude when sending to the LLM.
            exclude_embed (List[str]): Metadata keys to exclude when creating embeddings.
        """
        super().__init__(**kwargs)
        self.exclude_llm = exclude_llm
        self.exclude_embed = exclude_embed

    def __call__(self, nodes: List[BaseNode], **kwargs: Any) -> List[BaseNode]:
        """
        Applies the exclusion lists to the appropriate attributes of each node.
        """
        for node in nodes:
            # Update the list of metadata keys to exclude from LLM context
            node.excluded_llm_metadata_keys.extend(self.exclude_llm)
            # Update the list of metadata keys to exclude from embedding
            node.excluded_embed_metadata_keys.extend(self.exclude_embed)
        return nodes