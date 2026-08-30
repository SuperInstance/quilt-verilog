#!/usr/bin/env python3
"""mm.py -- multi-model client lib for the backend lane (stdlib only).

Endpoints (per TOOLS.md routing):
  flash()    DeepSeek V4-Flash   api.deepseek.com   deepseek-chat
  pro()      DeepSeek V4-Pro     api.deepseek.com   deepseek-reasoner
  seed()     Seed-2.0-mini       api.deepinfra.com  ByteDance/Seed-2.0-mini
  ollama()   local models        127.0.0.1:11434    qwen3:8b, deepseek-r1:8b

Keys come from the export lines in ~/.bashrc (DEEPSEEK_API_KEY,
DEEPINFRA_API_KEY) -- evaluated, not parsed, so quoting stays intact.
Every call returns (content, meta) or raises MMError; failures are
honest (no faking a voice that did not answer).
"""
import json
import os
import re
import time
import urllib.request


class MMError(Exception):
    pass


def _key(name):
    line = None
    with open(os.path.expanduser("~/.bashrc")) as f:
        for ln in f:
            if ln.strip().startswith("export %s=" % name):
                line = ln.strip()
                break
    if not line:
        raise MMError("%s not found in ~/.bashrc" % name)
    ns = {}
    exec(line[len("export "):].replace("=", "=", 1), ns)
    # strip 'export ' then exec 'NAME=value' (quotes handled by exec)
    val = ns.get(name, "")
    if not val or '"' in val[3:]:
        raise MMError("%s malformed" % name)
    return val


def _post(url, key, payload, timeout, retries=2):
    body = json.dumps(payload).encode()
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url, data=body,
                headers={"Authorization": "Bearer %s" % key,
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as ex:           # noqa: BLE001 - honest retry
            if attempt == retries:
                raise MMError("%s: %s" % (url, ex))
            time.sleep(2 * (attempt + 1))


def _chat(url, key, model, messages, timeout, **kw):
    payload = {"model": model, "messages": messages, **kw}
    d = _post(url, key, payload, timeout)
    if "choices" not in d:
        raise MMError("no choices: %s" % json.dumps(d)[:200])
    msg = d["choices"][0]["message"]
    return msg.get("content") or "", {
        "model": d.get("model"), "usage": d.get("usage", {}),
        "reasoning": (msg.get("reasoning_content") or "")[:4000],
    }


def flash(messages, timeout=120, **kw):
    return _chat("https://api.deepseek.com/chat/completions",
                 _key("DEEPSEEK_API_KEY"), "deepseek-chat",
                 messages, timeout, **kw)


def pro(messages, timeout=300, **kw):
    return _chat("https://api.deepseek.com/chat/completions",
                 _key("DEEPSEEK_API_KEY"), "deepseek-reasoner",
                 messages, timeout, **kw)


def seed(messages, timeout=120, **kw):
    return _chat("https://api.deepinfra.com/v1/openai/chat/completions",
                 _key("DEEPINFRA_API_KEY"), "ByteDance/Seed-2.0-mini",
                 messages, timeout, **kw)


def ollama(model, messages, timeout=300, think=False):
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"temperature": 0.2}}
    if think:
        payload["think"] = True
    d = _post("http://127.0.0.1:11434/api/chat", "x", payload, timeout)
    if "message" not in d:
        raise MMError("ollama: %s" % json.dumps(d)[:200])
    return d["message"].get("content") or "", {
        "model": model,
        "thinking": (d["message"].get("thinking") or "")[:4000],
    }


def extract_json(text):
    """pull the first JSON array/object out of a model reply"""
    m = re.search(r"```(?:json)?\s*([\[{].*?[\]}])\s*```", text, re.S)
    if not m:
        m = re.search(r"([\[{].*[\]}])", text, re.S)
    if not m:
        raise MMError("no JSON in reply: %s" % text[:200])
    return json.loads(m.group(1))
