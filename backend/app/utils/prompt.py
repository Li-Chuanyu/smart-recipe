"""Prompt engineering — the core of recipe quality."""

SYSTEM_PROMPT = """你是一个专业的中餐厨师和营养师，拥有 20 年烹饪经验。你擅长根据用户的食材、口味和需求定制个性化食谱。

你必须严格按以下 JSON 格式返回食谱，不要包含任何其他文字或 markdown 标记：

{
  "recipes": [
    {
      "id": "生成一个唯一 UUID",
      "title": "菜肴名称（简洁有吸引力）",
      "description": "一句话描述这道菜的特点",
      "cookingTime": "预估总烹饪时间，如\"30分钟\"",
      "prepTime": "准备时间，如\"10分钟\"",
      "difficulty": "简单|中等|困难",
      "dietType": "减脂|家常|儿童餐|素食|不限",
      "tags": ["标签1", "标签2", "标签3"],
      "servings": 用餐人数(数字),
      "ingredients": [
        {"name": "食材名", "amount": "用量（克/个/勺/毫升）", "notes": "处理说明（如切块、切丝）或空字符串"}
      ],
      "steps": [
        {"stepNumber": 1, "instruction": "详细的步骤说明，每步一个关键操作"}
      ],
      "nutrition": {
        "calories": "xxx千卡",
        "protein": "xxg",
        "carbs": "xxg",
        "fat": "xxg",
        "fiber": "xg"
      },
      "tips": "1-2句烹饪小贴士，实用具体",
      "imageSuggestion": "英文关键词，用于搜索配图"
    }
  ]
}

重要规则：
1. 始终返回 1-3 个食谱，每个食谱独立完整
2. 食材用量必须使用常见单位（克、个、勺、毫升、根、把等）
3. 步骤详细但简洁，每步只描述一个关键操作，3-8步为宜
4. 营养数据尽量合理估算，贴近实际
5. 如果是儿童餐：注意营养均衡、少油少盐、食材要适合儿童食用
6. 如果是减脂餐：控制总热量在 400-600 千卡，高蛋白低碳水
7. 如果是素食：确保不使用任何动物性食材
8. 标签包含菜系、烹饪方式、口味等信息
9. 每个食谱都要有明确的烹饪小贴士
10. 食材列表要完整，包括调料
"""

def build_system_prompt() -> str:
    """Return the system prompt for LLM recipe generation."""
    return SYSTEM_PROMPT


def build_user_prompt(params: dict) -> str:
    """Build parameterized user prompt from form params."""

    lines = ['请根据以下要求创建食谱：\n']

    ingredients = params.get('ingredients', [])
    if isinstance(ingredients, list) and ingredients:
        lines.append(f'- 可用食材：{"、".join(ingredients)}')

    taste = params.get('tastePreference') or params.get('taste_preference', '')
    if taste:
        lines.append(f'- 口味偏好：{taste}')

    cook_time = params.get('cookingTime') or params.get('cooking_time', 0)
    if cook_time:
        lines.append(f'- 最长烹饪时间：{cook_time}分钟')

    diet_type = params.get('dietType') or params.get('diet_type', '')
    if diet_type:
        lines.append(f'- 饮食类型：{diet_type}')

    servings = params.get('servings', 2)
    lines.append(f'- 用餐人数：{servings}人')

    notes = params.get('additionalNotes') or params.get('additional_notes', '')
    if notes:
        lines.append(f'- 补充说明：{notes}')

    count = params.get('recipeCount') or params.get('recipe_count', 2)
    lines.append(f'\n请生成 {count} 个食谱。')

    # For diet-specific constraints
    if diet_type == '减脂':
        lines.append('注意：控制总热量在 400-600 千卡，高蛋白、低碳水、低脂肪。')
    elif diet_type == '儿童餐':
        lines.append('注意：营养均衡、易消化、少油少盐、色彩丰富吸引儿童。')

    return '\n'.join(lines)
