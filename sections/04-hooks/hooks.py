"""Hooks (section 4): PreToolUse / PostToolUse interception around tool calls.

A PreToolUse hook may block a call or rewrite its input; it cannot grant
permission a call lacks (so hooks here only deny or modify, never allow).
PostToolUse hooks observe results. Mirrors Claude Code's types/hooks.ts.
"""

PRE_TOOL_USE, POST_TOOL_USE = "PreToolUse", "PostToolUse"


class Hooks:
    def __init__(self):
        self._hooks = {PRE_TOOL_USE: [], POST_TOOL_USE: []}
        self._events = [PRE_TOOL_USE, POST_TOOL_USE]

    def register(self, event, fn):
        """register hooks"""
        if event not in self._events:
            raise RuntimeError(f"Error: {event} not allowed")
        self._hooks[event] = fn

    def fire_pre(self, name, args):
        """hooks before permission gate"""
        for fn in self._hooks["PreToolUse"]:
            res = fn(name, args) or {}
            if res.get("updated_args"):
                args = res["updated_args"]
            if res.get("deny"):
                return True, args, res.get("message")
            return False, args, ""

    def fire_post(self, name, args):
        """hooks after tool use"""
        for fn in self._hooks["PostToolUse"]:
            fn(name, args)
