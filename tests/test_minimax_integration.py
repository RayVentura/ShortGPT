"""Integration tests for MiniMax LLM and TTS providers.

These tests require a valid MINIMAX_API_KEY environment variable.
They are skipped automatically when the key is not available.
"""

import os
import tempfile

import pytest

MINIMAX_API_KEY = os.environ.get('MINIMAX_API_KEY', '')
skip_no_key = pytest.mark.skipif(not MINIMAX_API_KEY, reason='MINIMAX_API_KEY not set')


@skip_no_key
class TestMiniMaxLLMIntegration:
    """Integration tests for MiniMax LLM via OpenAI-compatible API."""

    def test_basic_chat_completion(self):
        """Should complete a basic chat request using MiniMax API."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url='https://api.minimax.io/v1',
        )
        response = client.chat.completions.create(
            model='MiniMax-M2.7',
            messages=[{'role': 'user', 'content': 'Say "test passed" and nothing else.'}],
            max_tokens=20,
            temperature=1.0,
        )
        assert response.choices[0].message.content
        assert len(response.choices[0].message.content.strip()) > 0

    def test_chat_completion_with_system_message(self):
        """Should handle system + user messages."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url='https://api.minimax.io/v1',
        )
        response = client.chat.completions.create(
            model='MiniMax-M2.7',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant. Reply with exactly one word.'},
                {'role': 'user', 'content': 'What color is the sky?'},
            ],
            max_tokens=10,
            temperature=1.0,
        )
        assert response.choices[0].message.content
        assert len(response.choices[0].message.content.strip()) > 0

    def test_streaming_chat_completion(self):
        """Should handle streaming responses."""
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url='https://api.minimax.io/v1',
        )
        stream = client.chat.completions.create(
            model='MiniMax-M2.7',
            messages=[{'role': 'user', 'content': 'Count from 1 to 3.'}],
            max_tokens=30,
            temperature=1.0,
            stream=True,
        )
        chunks = []
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                chunks.append(chunk.choices[0].delta.content)
        assert len(chunks) > 0


@skip_no_key
class TestMiniMaxTTSIntegration:
    """Integration tests for MiniMax TTS voice module."""

    def test_generate_voice_produces_audio_file(self):
        """Should generate a valid MP3 audio file."""
        from shortGPT.audio.minimax_voice_module import MiniMaxVoiceModule

        module = MiniMaxVoiceModule(api_key=MINIMAX_API_KEY)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            output_file = f.name

        try:
            result = module.generate_voice('Hello, this is a test of MiniMax TTS.', output_file)
            assert result == output_file
            assert os.path.exists(output_file)
            file_size = os.path.getsize(output_file)
            assert file_size > 100, f'Audio file too small: {file_size} bytes'
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_voice_with_different_voice(self):
        """Should generate audio with a different voice ID."""
        from shortGPT.audio.minimax_voice_module import MiniMaxVoiceModule

        module = MiniMaxVoiceModule(
            api_key=MINIMAX_API_KEY,
            voice_id='English_Persuasive_Man',
        )
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            output_file = f.name

        try:
            result = module.generate_voice('Testing voice module.', output_file)
            assert result == output_file
            assert os.path.getsize(output_file) > 100
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_voice_invalid_key_raises(self):
        """Should raise exception with invalid API key."""
        from shortGPT.audio.minimax_voice_module import MiniMaxVoiceModule

        module = MiniMaxVoiceModule(api_key='invalid-key-12345')
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            output_file = f.name

        try:
            with pytest.raises(Exception):
                module.generate_voice('Hello', output_file)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)
