from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore
from llama_index.core import QueryBundle
from typing import Optional

class UniqueNodePostprocessor(BaseNodePostprocessor):
    """Remove redundant nodes that have identical start and end character indices."""


    def _postprocess_nodes(self, nodes: list[NodeWithScore],  query_bundle: Optional[QueryBundle]) -> list[NodeWithScore]:
        seen_spans = set()
        unique_nodes = []
        print(f"nodes befor uniqueness.{len(nodes)}")
        for node in nodes:
            start = getattr(node.node, "start_char_idx", None)
            end = getattr(node.node, "end_char_idx", None)

            if start is  None or end is None:
                unique_nodes.append(node)
            else:
                span_key = (start, end)
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    unique_nodes.append(node)
        print(f"nodes after uniqueness.{len(unique_nodes)}")

        return unique_nodes
