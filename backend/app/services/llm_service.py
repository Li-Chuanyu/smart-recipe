import hashlib
import json
from typing import Generator
from openai import OpenAI
from flask import current_app
from app.services.cache_service import CacheService
from app.utils.prompt import build_system_prompt, build_user_prompt
from app.utils.parser import parse_recipe_response

class LLMService:
    """Large Language Model API wrapper for recipe generation."""

    SUPPORTED_MODELS = {
        'gpt-4o-mini':   {'provider': 'openai', 'max_tokens': 4096},
        'gpt-4o':        {'provider': 'openai', 'max_tokens': 8192},
        'deepseek-v4-flash': {'provider': 'deepseek', 'max_tokens': 4096},
        'deepseek-v4-pro': {'provider': 'deepseek', 'max_tokens': 4096},
        'qwen-plus':     {'provider': 'qwen', 'max_tokens': 4096},
        'claude-3-haiku': {'provider': 'anthropic', 'max_tokens': 4096},
    }

    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
        self.model = current_app.config.get('LLM_DEFAULT_MODEL', 'gpt-4o-mini')
        self.api_key = current_app.config.get('LLM_API_KEY', '')
        self.api_base = current_app.config.get('LLM_API_BASE', 'https://api.openai.com')

    def _build_client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key, base_url=self.api_base)

    def _hash_params(self, params: dict) -> str:
        """Create MD5 hash of sorted parameters for caching."""
        raw = json.dumps(params, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(raw.encode('utf-8')).hexdigest()

    def generate(self, params: dict, model: str | None = None) -> tuple[list | None, str | None]:
        """
        Generate recipes synchronously.
        Returns (recipes_list, error_message).
        """
        model = model or self.model

        # 1. Hash params for caching
        prompt_hash = self._hash_params(params)

        # 2. Check Redis cache
        cached = self.cache.get_recipe(prompt_hash)
        if cached:
            return cached, None

        # 3. Build messages
        messages = [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(params)},
        ]

        # 4. Call LLM API
        try:
            client = self._build_client()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.8,
                max_tokens=2048,
                response_format={"type": "json_object"},
                timeout=90,
            )
            content = response.choices[0].message.content
        except Exception as e:
            error_msg = self._normalize_error(e)
            return None, error_msg

        # 5. Parse and validate
        recipes = parse_recipe_response(content)
        if not recipes:
            return None, 'AI 返回了无法解析的格式，请重试'

        # 6. Cache result
        self.cache.set_recipe(prompt_hash, recipes)

        return recipes, None

    def generate_stream(self, params: dict, model: str | None = None) -> Generator[str, None, None]:
        """
        Generate recipes with SSE streaming.
        Yields text chunks; caller should buffer and parse on completion.
        """
        model = model or self.model
        prompt_hash = self._hash_params(params)

        # Check cache first (stream the cached result if exists)
        cached = self.cache.get_recipe(prompt_hash)
        if cached:
            yield json.dumps(cached, ensure_ascii=False)
            return

        messages = [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(params)},
        ]

        try:
            client = self._build_client()
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.8,
                max_tokens=2048,
                stream=True,
                timeout=120,
            )
            buffer = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    buffer += token
                    yield token

            # Cache the complete result after streaming
            recipes = parse_recipe_response(buffer)
            if recipes:
                self.cache.set_recipe(prompt_hash, recipes)

        except Exception as e:
            yield f"\n__ERROR__:{self._normalize_error(e)}"

    def _normalize_error(self, error: Exception) -> str:
        """Convert various API errors to user-friendly messages."""
        error_str = str(error).lower()

        if '401' in error_str or 'unauthorized' in error_str or 'invalid api key' in error_str:
            return 'API 密钥无效，请检查后端配置'
        if '429' in error_str or 'rate limit' in error_str:
            return '请求过于频繁，请稍后重试'
        if 'timeout' in error_str or 'timed out' in error_str:
            return 'AI 服务响应超时，请重试'
        if '500' in error_str or 'server error' in error_str:
            return 'AI 服务暂时不可用，请稍后重试'
        if 'connection' in error_str or 'network' in error_str:
            return '无法连接到 AI 服务，请检查网络'

        return f'AI 调用失败: {str(error)[:200]}'
