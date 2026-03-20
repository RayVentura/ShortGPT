"""Unit tests for MiniMax LLM provider integration in gpt_utils."""

import os
from unittest.mock import MagicMock, patch

import pytest


class TestMiniMaxLLMProvider:
    """Tests for MiniMax LLM integration in gpt_utils.llm_completion."""

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    @patch('shortGPT.gpt.gpt_utils.OpenAI')
    def test_minimax_selected_when_key_present_and_no_gemini(self, mock_openai_cls, mock_key_mgr):
        """MiniMax should be selected when MINIMAX_API_KEY is set and no Gemini key."""
        mock_key_mgr.get_api_key.side_effect = lambda key: {
            'OPENAI_API_KEY': '',
            'GEMINI_API_KEY': '',
            'MINIMAX_API_KEY': 'test-minimax-key',
        }.get(key, '')

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Hello from MiniMax'
        mock_client.chat.completions.create.return_value = mock_response

        from shortGPT.gpt.gpt_utils import llm_completion
        result = llm_completion(chat_prompt="Hi", system="You are helpful")

        mock_openai_cls.assert_called_once_with(
            api_key='test-minimax-key',
            base_url='https://api.minimax.io/v1'
        )
        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs[1]['model'] == 'MiniMax-M2.7'
        assert result == 'Hello from MiniMax'

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    @patch('shortGPT.gpt.gpt_utils.OpenAI')
    def test_gemini_takes_priority_over_minimax(self, mock_openai_cls, mock_key_mgr):
        """Gemini should be selected over MiniMax when both keys are present."""
        mock_key_mgr.get_api_key.side_effect = lambda key: {
            'OPENAI_API_KEY': '',
            'GEMINI_API_KEY': 'test-gemini-key',
            'MINIMAX_API_KEY': 'test-minimax-key',
        }.get(key, '')

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Hello from Gemini'
        mock_client.chat.completions.create.return_value = mock_response

        from shortGPT.gpt.gpt_utils import llm_completion
        llm_completion(chat_prompt="Hi", system="You are helpful")

        mock_openai_cls.assert_called_once_with(
            api_key='test-gemini-key',
            base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
        )

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    @patch('shortGPT.gpt.gpt_utils.OpenAI')
    def test_minimax_takes_priority_over_openai(self, mock_openai_cls, mock_key_mgr):
        """MiniMax should be selected over OpenAI when both keys are present (no Gemini)."""
        mock_key_mgr.get_api_key.side_effect = lambda key: {
            'OPENAI_API_KEY': 'test-openai-key',
            'GEMINI_API_KEY': '',
            'MINIMAX_API_KEY': 'test-minimax-key',
        }.get(key, '')

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Hello'
        mock_client.chat.completions.create.return_value = mock_response

        from shortGPT.gpt.gpt_utils import llm_completion
        llm_completion(chat_prompt="Hi", system="You are helpful")

        mock_openai_cls.assert_called_once_with(
            api_key='test-minimax-key',
            base_url='https://api.minimax.io/v1'
        )

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    @patch('shortGPT.gpt.gpt_utils.OpenAI')
    def test_minimax_temperature_clamping_zero(self, mock_openai_cls, mock_key_mgr):
        """MiniMax should clamp temperature=0 to 0.01."""
        mock_key_mgr.get_api_key.side_effect = lambda key: {
            'OPENAI_API_KEY': '',
            'GEMINI_API_KEY': '',
            'MINIMAX_API_KEY': 'test-key',
        }.get(key, '')

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'OK'
        mock_client.chat.completions.create.return_value = mock_response

        from shortGPT.gpt.gpt_utils import llm_completion
        llm_completion(chat_prompt="Hi", system="test", temp=0.0)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['temperature'] == 0.01

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    @patch('shortGPT.gpt.gpt_utils.OpenAI')
    def test_minimax_temperature_clamping_high(self, mock_openai_cls, mock_key_mgr):
        """MiniMax should clamp temperature > 1.0 to 1.0."""
        mock_key_mgr.get_api_key.side_effect = lambda key: {
            'OPENAI_API_KEY': '',
            'GEMINI_API_KEY': '',
            'MINIMAX_API_KEY': 'test-key',
        }.get(key, '')

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'OK'
        mock_client.chat.completions.create.return_value = mock_response

        from shortGPT.gpt.gpt_utils import llm_completion
        llm_completion(chat_prompt="Hi", system="test", temp=1.5)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['temperature'] == 1.0

    @patch('shortGPT.gpt.gpt_utils.ApiKeyManager')
    def test_no_keys_raises_exception(self, mock_key_mgr):
        """Should raise exception when no API keys are configured."""
        mock_key_mgr.get_api_key.return_value = ''

        from shortGPT.gpt.gpt_utils import llm_completion
        with pytest.raises(Exception, match="No OpenAI, Gemini, or MiniMax API Key"):
            llm_completion(chat_prompt="Hi", system="test")


class TestTokenCounting:
    """Tests for num_tokens_from_messages with non-OpenAI models."""

    def test_token_count_with_unknown_model_falls_back(self):
        """Should use cl100k_base encoding for unknown models like MiniMax."""
        from shortGPT.gpt.gpt_utils import num_tokens_from_messages
        # Should not raise NotImplementedError for MiniMax model
        count = num_tokens_from_messages("Hello world", model="MiniMax-M2.7")
        assert count > 0

    def test_token_count_with_string_input(self):
        """Should handle string input."""
        from shortGPT.gpt.gpt_utils import num_tokens_from_messages
        count = num_tokens_from_messages("Hello world")
        assert count > 0

    def test_token_count_with_list_input(self):
        """Should handle list of strings input."""
        from shortGPT.gpt.gpt_utils import num_tokens_from_messages
        count = num_tokens_from_messages(["Hello", "world"])
        assert count > 0


class TestApiProviderEnum:
    """Tests for MiniMax in ApiProvider enum."""

    def test_minimax_in_api_provider(self):
        """MINIMAX should be in the ApiProvider enum."""
        from shortGPT.config.api_db import ApiProvider
        assert hasattr(ApiProvider, 'MINIMAX')
        assert ApiProvider.MINIMAX.value == 'MINIMAX_API_KEY'
