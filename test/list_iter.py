def print_token_list_depth(token, current_depth=0):
    """
    재귀적으로 토큰 트리를 순회하며, 각 토큰이 속한 리스트의 깊이를 출력합니다.

    인자:
      token: 토큰을 나타내는 dict 또는 list
      current_depth: 현재 리스트 깊이 (초기값 0)
    """
    if isinstance(token, dict):
        token_type = token.get("type")
        # 토큰 타입이 있을 경우 리스트 깊이를 출력합니다.
        if token_type:
            print(f"토큰 타입: {token_type} - 리스트 깊이: {current_depth}")
        # 만약 이 토큰이 'list' 타입이면, 자식 토큰의 리스트 깊이를 1 증가시킵니다.
        if token_type == "list":
            new_depth = current_depth + 1
        else:
            new_depth = current_depth
        # 자식 토큰을 재귀적으로 처리합니다.
        for child in token.get("children", []):
            print_token_list_depth(child, new_depth)
    elif isinstance(token, list):
        for item in token:
            print_token_list_depth(item, current_depth)


# 예제 토큰 (사용자가 제공한 JSON 구조)
example_token = {
    "type": "list",
    "children": [
        {
            "type": "list_item",
            "children": [
                {
                    "type": "block_text",
                    "children": [
                        {
                            "type": "text",
                            "raw": "LLM을 구동하는 데에는 많은 자원이 필요하며, 대화가 길어지면 긴 대화를 처리하기 어려워함",
                        }
                    ],
                }
            ],
        },
        {
            "type": "list_item",
            "children": [
                {
                    "type": "block_text",
                    "children": [
                        {
                            "type": "text",
                            "raw": "답변의 생성은 매번 독립시행임을 생각할 때",
                        }
                    ],
                },
                {
                    "type": "list",
                    "children": [
                        {
                            "type": "list_item",
                            "children": [
                                {
                                    "type": "block_text",
                                    "children": [
                                        {
                                            "type": "text",
                                            "raw": "기존의 대화를 요약해서 사전 프롬프트(pre-prompt)로 제공하고 있을 것",
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "children": [
                                {
                                    "type": "block_text",
                                    "children": [
                                        {
                                            "type": "link",
                                            "children": [
                                                {
                                                    "type": "text",
                                                    "raw": "Exposing pre-prompt",
                                                }
                                            ],
                                            "attrs": {
                                                "url": "https://www.reddit.com/r/ChatGPT/comments/12fnqhd/exposing_preprompt/?rdt=53762"
                                            },
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "list_item",
                            "children": [
                                {
                                    "type": "block_text",
                                    "children": [
                                        {
                                            "type": "link",
                                            "children": [
                                                {
                                                    "type": "text",
                                                    "raw": "Gaslighting AI into 2+2=5",
                                                }
                                            ],
                                            "attrs": {
                                                "url": "https://www.youtube.com/watch?v=3wlvNfTNgB8"
                                            },
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                    "tight": True,
                    "bullet": "-",
                    "attrs": {"depth": 1, "ordered": False},
                },
            ],
        },
    ],
}

# 함수 실행: 토큰 트리 전체에 대해 리스트 깊이 출력
print_token_list_depth(example_token)
