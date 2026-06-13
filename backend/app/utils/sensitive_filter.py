"""敏感词过滤工具（DFA算法）"""

from typing import List, Tuple


class SensitiveFilter:
    """基于DFA算法的敏感词过滤器"""

    def __init__(self):
        self._root = {}
        self._initialized = False

    def build(self, words: List[str]):
        """构建DFA树"""
        self._root = {}
        for word in words:
            self._add_word(word)
        self._initialized = True

    def _add_word(self, word: str):
        """添加一个敏感词到DFA树"""
        node = self._root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node["\0"] = None  # 标记结尾

    def filter(self, text: str, replace_char: str = "*") -> str:
        """过滤敏感词，返回替换后的文本"""
        if not self._initialized:
            return text

        result = list(text)
        i = 0
        while i < len(text):
            node = self._root
            if text[i] not in node:
                i += 1
                continue

            j = i
            matched = False
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if "\0" in node:
                    matched = True
                    end = j
                j += 1

            if matched:
                for k in range(i, end + 1):
                    result[k] = replace_char
                i = end + 1
            else:
                i += 1

        return "".join(result)

    def contains_sensitive(self, text: str) -> bool:
        """检查是否包含敏感词"""
        if not self._initialized:
            return False

        i = 0
        while i < len(text):
            node = self._root
            if text[i] not in node:
                i += 1
                continue

            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if "\0" in node:
                    return True
                j += 1
            i += 1

        return False

    def find_all(self, text: str) -> List[Tuple[str, int, int]]:
        """找出所有敏感词及其位置"""
        result = []
        if not self._initialized:
            return result

        i = 0
        while i < len(text):
            node = self._root
            if text[i] not in node:
                i += 1
                continue

            j = i
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                if "\0" in node:
                    result.append((text[i:j + 1], i, j))
                j += 1
            i += 1

        return result


# 全局单例
sensitive_filter = SensitiveFilter()
