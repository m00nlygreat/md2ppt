def plugin_comment_block(md):
    # 패턴 문자열로 정의합니다.
    # pattern = r'^\[(?P<key>[^\]]+)\]:\s*#\s*\((?P<value>[^)]+)\)\s*$'
    pattern = r'^\[(?P<key>[^\]]+)\]:\s*#\s*\((?P<value>.+)\)\s*$'
    # 콜백 함수는 (self, m, state)를 받고, 토큰을 상태에 추가한 후 새 커서 위치를 정수로 반환해야 합니다.
    def parse_comment_block(self, m, state):
        token = {
            'type': 'comment_block',
            'key': m.group('key'),
            'value': m.group('value'),
            'raw': m.group(0).replace('\n','')
        }
        state.append_token(token)
        return m.end()
    
    # 'ref_link'보다 먼저 처리되도록 등록합니다.
    md.block.register('comment_block', pattern, parse_comment_block, before='ref_link')
    return md