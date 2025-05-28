import unittest
from unittest.mock import patch
from langchain.schema import Document
from agentic_rag import (
    retrieve_info,
    gera_multiplas_respostas,
    avalia_similaridade,
    rank_respostas,
    AgentState,
)

class TestAgenticRAGCase10(unittest.TestCase):

    @patch("agentic_rag.retriever")
    def test_retrieve_info(self, mock_retriever):
        mock_retriever.invoke.return_value = [Document(page_content="conteúdo")]
        state = AgentState(query="exemplo")
        new_state = retrieve_info(state)
        mock_retriever.invoke.assert_called_once_with("exemplo")
        self.assertEqual(len(new_state.retrieved_info), 1)

    @patch("agentic_rag.qa_chain")
    def test_gera_multiplas_respostas(self, mock_chain):
        mock_chain.invoke.return_value = "resposta"
        state = AgentState(query="exemplo")
        new_state = gera_multiplas_respostas(state)
        self.assertEqual(len(new_state.possible_responses), 5)

    @patch("agentic_rag.embedding_model")
    def test_avalia_similaridade(self, mock_embedding_model):
        mock_embedding_model.embed_documents.return_value = [[0.1]*768]
        state = AgentState(
            query="exemplo",
            retrieved_info=[Document(page_content="texto")],
            possible_responses=["resposta"]
        )
        new_state = avalia_similaridade(state)
        self.assertEqual(len(new_state.similarity_scores), 1)

    def test_rank_respostas(self):
        state = AgentState(
            query="exemplo",
            possible_responses=["resp1", "resp2"],
            similarity_scores=[0.7, 0.9]
        )
        new_state = rank_respostas(state)
        self.assertEqual(new_state.ranked_response, "resp2")
        self.assertEqual(new_state.confidence_score, 0.9)

if __name__ == '__main__':
    unittest.main(verbosity=2)
