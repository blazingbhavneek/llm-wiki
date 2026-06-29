"""Mermaid diagram validation + repair for chat answers.

Graph-side, LLM-library-free: validates a Mermaid block by actually rendering it
with ``mmdc`` (mermaid-cli + Chrome headless, same setup as ``image.py``), and if
it fails, asks the injected llm client to repair it — looping until it renders or
the attempt budget runs out.

Only used when ``Settings.enable_mermaid`` is on. The lead agent's compiled answer
may contain a ```mermaid block; this fixes that block in place before the UI shows
it as a diagram artifact.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

# Appended to the lead/compile prompt ONLY when enable_mermaid is on.
MERMAID_INSTRUCTION = (
    "\n\nDiagrams:\n"
    "- If a flowchart, architecture/block diagram, sequence, or data-flow diagram "
    "would make the answer clearer, include ONE Mermaid diagram in a ```mermaid "
    "fenced block as part of your answer.\n"
    "- Only add a diagram when it genuinely helps; skip it otherwise.\n"
    "- Use simple ASCII node IDs (n1, n2, proc_a) and put any spaces/punctuation/"
    "long text inside quoted labels: n1[\"Linear layer\"] --> n2[\"GEMM\"].\n"
    "- The mermaid block must contain ONLY Mermaid syntax (no prose/bullets)."
)

_MERMAID_BLOCK_RE = re.compile(
    r"```mermaid[ \t]*\r?\n(?P<code>.*?)```",
    re.IGNORECASE | re.DOTALL,
)

_FIX_SYSTEM = (
    "You fix Mermaid diagram syntax so it renders with mermaid-cli (mmdc). "
    "Return ONLY one corrected ```mermaid fenced code block and nothing else."
)


def has_mermaid(text: str) -> bool:
    return bool(_MERMAID_BLOCK_RE.search(text or ""))


def validate_mermaid(code: str, settings: Any) -> tuple[bool, str]:
    """Render the code to SVG with mmdc; True if it parses+renders."""
    mmdc = shutil.which(settings.mermaid_cli_bin)
    if mmdc is None:
        return False, f"mermaid CLI '{settings.mermaid_cli_bin}' not found in PATH"

    config = Path(settings.mermaid_puppeteer_config).expanduser()
    cmd_prefix = [mmdc]
    if config.exists():
        cmd_prefix += ["-p", str(config)]

    with tempfile.TemporaryDirectory() as tmp:
        in_file = Path(tmp) / "d.mmd"
        out_file = Path(tmp) / "d.svg"
        in_file.write_text(code, encoding="utf-8")
        cmd = [*cmd_prefix, "-i", str(in_file), "-o", str(out_file)]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                timeout=settings.mermaid_render_timeout,
            )
        except subprocess.TimeoutExpired:
            return False, f"mmdc timed out after {settings.mermaid_render_timeout}s"
        except Exception as exc:  # noqa: BLE001 - mmdc failed to start
            return False, f"mmdc failed to start: {exc}"

        if proc.returncode == 0 and out_file.exists() and out_file.stat().st_size > 0:
            return True, ""
        return False, proc.stderr.decode("utf-8", errors="replace").strip()


def _repair_once(llm: Any, code: str, error: str, settings: Any) -> str | None:
    user = (
        "The following Mermaid diagram does not render. Fix the syntax, preserving "
        "all nodes, edges, directions, and labels. Use simple ASCII node IDs and "
        "quoted labels for any spaces/punctuation/long text.\n\n"
        f"Render error:\n{error}\n\n"
        f"```mermaid\n{code}\n```"
    )
    try:
        response = llm.complete(_FIX_SYSTEM, user)
    except Exception:  # noqa: BLE001 - repair is best-effort
        return None
    match = _MERMAID_BLOCK_RE.search(response)
    if match:
        return match.group("code").strip()
    cleaned = response.strip().strip("`").strip()
    return cleaned or None


def repair_answer_mermaid(
    answer: str,
    llm: Any,
    settings: Any,
    emit: Callable[[dict], None],
) -> str:
    """Validate + repair every mermaid block in `answer`; emit progress events.

    Returns the answer with each block replaced by its best (ideally rendering)
    version. Emits diagram_pending -> diagram_ready / diagram_failed.
    """
    blocks = list(_MERMAID_BLOCK_RE.finditer(answer))
    if not blocks:
        return answer

    emit({"type": "diagram_pending"})

    new_answer = answer
    fixed_codes: list[str] = []
    all_ok = True

    for match in blocks:
        original_block = match.group(0)
        code = match.group("code").strip()
        ok, error = validate_mermaid(code, settings)
        attempt = 0
        while not ok and attempt < settings.mermaid_repair_attempts:
            attempt += 1
            repaired = _repair_once(llm, code, error, settings)
            if not repaired:
                break
            code = repaired
            ok, error = validate_mermaid(code, settings)

        all_ok = all_ok and ok
        fixed_codes.append(code)
        new_answer = new_answer.replace(
            original_block, f"```mermaid\n{code}\n```", 1
        )

    if all_ok:
        emit({"type": "diagram_ready", "answer": new_answer, "mermaid": fixed_codes})
    else:
        emit({"type": "diagram_failed", "answer": new_answer})

    return new_answer
