"""Unit tests for MiniMax TTS voice module."""

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from shortGPT.audio.minimax_voice_module import (
    MINIMAX_TTS_VOICES,
    MiniMaxVoiceModule,
)


class TestMiniMaxVoiceModuleInit:
    """Tests for MiniMaxVoiceModule initialization."""

    def test_default_initialization(self):
        """Should initialize with default parameters."""
        module = MiniMaxVoiceModule(api_key='test-key')
        assert module.api_key == 'test-key'
        assert module.voice_id == 'English_Graceful_Lady'
        assert module.model == 'speech-2.8-hd'
        assert module.base_url == 'https://api.minimax.io'

    def test_custom_voice_id(self):
        """Should accept custom voice_id."""
        module = MiniMaxVoiceModule(api_key='test-key', voice_id='English_Persuasive_Man')
        assert module.voice_id == 'English_Persuasive_Man'

    def test_custom_model(self):
        """Should accept custom model."""
        module = MiniMaxVoiceModule(api_key='test-key', model='speech-2.8-turbo')
        assert module.model == 'speech-2.8-turbo'

    def test_remaining_characters_unlimited(self):
        """MiniMax TTS has no character limit tracking."""
        module = MiniMaxVoiceModule(api_key='test-key')
        assert module.get_remaining_characters() == 999999999999

    def test_update_usage_returns_none(self):
        """MiniMax TTS doesn't track usage."""
        module = MiniMaxVoiceModule(api_key='test-key')
        assert module.update_usage() is None


class TestMiniMaxVoiceModuleGenerate:
    """Tests for MiniMaxVoiceModule.generate_voice."""

    @patch('shortGPT.audio.minimax_voice_module.requests.post')
    def test_generate_voice_success(self, mock_post, tmp_path):
        """Should generate audio file from TTS API response."""
        # "ID3" MP3 header in hex
        hex_audio = '494433'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {'audio': hex_audio, 'status': 2},
            'base_resp': {'status_code': 0, 'status_msg': 'success'},
        }
        mock_post.return_value = mock_response

        module = MiniMaxVoiceModule(api_key='test-key')
        output_file = str(tmp_path / 'test_output.mp3')
        result = module.generate_voice('Hello world', output_file)

        assert result == output_file
        assert os.path.exists(output_file)
        with open(output_file, 'rb') as f:
            content = f.read()
        assert content == bytes.fromhex(hex_audio)

    @patch('shortGPT.audio.minimax_voice_module.requests.post')
    def test_generate_voice_sends_correct_request(self, mock_post, tmp_path):
        """Should send correct request to MiniMax TTS API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {'audio': '494433', 'status': 2},
            'base_resp': {'status_code': 0, 'status_msg': 'success'},
        }
        mock_post.return_value = mock_response

        module = MiniMaxVoiceModule(api_key='test-api-key', voice_id='English_Persuasive_Man', model='speech-2.8-hd')
        output_file = str(tmp_path / 'test.mp3')
        module.generate_voice('Test text', output_file)

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == 'https://api.minimax.io/v1/t2a_v2'
        assert call_args[1]['headers']['Authorization'] == 'Bearer test-api-key'

        payload = json.loads(call_args[1]['data'])
        assert payload['model'] == 'speech-2.8-hd'
        assert payload['text'] == 'Test text'
        assert payload['stream'] is False
        assert payload['voice_setting']['voice_id'] == 'English_Persuasive_Man'
        assert payload['audio_setting']['format'] == 'mp3'

    @patch('shortGPT.audio.minimax_voice_module.requests.post')
    def test_generate_voice_http_error(self, mock_post):
        """Should raise exception on HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_post.return_value = mock_response

        module = MiniMaxVoiceModule(api_key='bad-key')
        with pytest.raises(Exception, match='MiniMax TTS error: 401'):
            module.generate_voice('Hello', '/tmp/test.mp3')

    @patch('shortGPT.audio.minimax_voice_module.requests.post')
    def test_generate_voice_api_error(self, mock_post):
        """Should raise exception on API error response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {},
            'base_resp': {'status_code': 1004, 'status_msg': 'Invalid API key'},
        }
        mock_post.return_value = mock_response

        module = MiniMaxVoiceModule(api_key='bad-key')
        with pytest.raises(Exception, match='Invalid API key'):
            module.generate_voice('Hello', '/tmp/test.mp3')

    @patch('shortGPT.audio.minimax_voice_module.requests.post')
    def test_generate_voice_no_audio_data(self, mock_post):
        """Should raise exception when no audio in response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {},
            'base_resp': {'status_code': 0, 'status_msg': 'success'},
        }
        mock_post.return_value = mock_response

        module = MiniMaxVoiceModule(api_key='test-key')
        with pytest.raises(Exception, match='no audio data'):
            module.generate_voice('Hello', '/tmp/test.mp3')


class TestMiniMaxTTSVoices:
    """Tests for MiniMax TTS voice definitions."""

    def test_voice_dict_not_empty(self):
        """Voice dictionary should have entries."""
        assert len(MINIMAX_TTS_VOICES) > 0

    def test_default_voice_exists(self):
        """Default voice should be in the dictionary."""
        assert 'English_Graceful_Lady' in MINIMAX_TTS_VOICES

    def test_known_voices_present(self):
        """Known valid voice IDs should be present."""
        expected_voices = [
            'English_Graceful_Lady',
            'English_Insightful_Speaker',
            'English_radiant_girl',
            'English_Persuasive_Man',
            'English_Lucky_Robot',
        ]
        for voice in expected_voices:
            assert voice in MINIMAX_TTS_VOICES

    def test_voice_module_inherits_from_abc(self):
        """MiniMaxVoiceModule should inherit from VoiceModule ABC."""
        from shortGPT.audio.voice_module import VoiceModule
        assert issubclass(MiniMaxVoiceModule, VoiceModule)
