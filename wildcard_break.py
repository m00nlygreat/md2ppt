import re

def wildcard_break_plugin(md):
    """ ***을 `wildcard_break`으로 구분하고, `thematic_break`에서 제거하는 플러그인 """

    # 1️⃣ 기존 `thematic_break`에서 `***`을 제외한 새로운 정규식
    THEMATIC_BREAK_PATTERN = r'^(?:---|___)\s*$'

    # 2️⃣ `***`만 따로 처리하는 새로운 정규식
    WILDCARD_BREAK_PATTERN = r'^\*\*\*\s*$'

    def parse_thematic_break(block, m, state):
        """ --- 또는 ___ 만 `thematic_break`으로 처리 """
        state.append_token({'type': 'thematic_break'})
        return m.end()

    def parse_wildcard_break(block, m, state):
        """ ***을 `wildcard_break`으로 처리 """
        state.append_token({'type': 'wildcard_break'})
        return m.end()

    # 3️⃣ 기존 `thematic_break`을 새 패턴으로 덮어쓰기
    md.block.register('thematic_break', THEMATIC_BREAK_PATTERN, parse_thematic_break)

    # 4️⃣ `***`을 `wildcard_break`으로 추가
    md.block.register('wildcard_break', WILDCARD_BREAK_PATTERN, parse_wildcard_break, before="thematic_break")