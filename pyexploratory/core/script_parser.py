"""
Reverse-parse an exported PyExploratory script back into action log entries.

Pure business logic — NO Dash imports.  Takes script text, returns a list of
dicts identical in shape to those produced by ``action_log.log_action()``.
"""

import ast
import re
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Section anchor patterns
# ---------------------------------------------------------------------------
_SECTION_RE = re.compile(
    r"^# --- (Load data|Data cleaning|Charts|Machine Learning) ---\s*$",
    re.MULTILINE,
)
_CHART_SUB_RE = re.compile(r"^# --- Chart: (\w+) ---\s*$", re.MULTILINE)
_ML_SUB_RE = re.compile(r"^# --- ML: (\w+) ---\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_literal(s: str):
    """Safely evaluate a Python literal (string, number, None)."""
    try:
        return ast.literal_eval(s.strip())
    except (ValueError, SyntaxError):
        return s.strip().strip("'\"")


def _extract_between(text: str, start_re, end_re=None) -> str:
    """Return text between *start_re* match and *end_re* match (or EOF)."""
    m = start_re.search(text)
    if not m:
        return ""
    rest = text[m.end() :]
    if end_re:
        m2 = end_re.search(rest)
        if m2:
            return rest[: m2.start()]
    return rest


def _split_sections(text: str) -> Dict[str, str]:
    """Split script text into named section bodies."""
    anchors = [
        "# --- Load data ---",
        "# --- Data cleaning ---",
        "# --- Charts ---",
        "# --- Machine Learning ---",
    ]
    sections: Dict[str, str] = {}
    for i, anchor in enumerate(anchors):
        pos = text.find(anchor)
        if pos == -1:
            continue
        start = pos + len(anchor)
        # Find the next anchor (or EOF)
        end = len(text)
        for next_anchor in anchors[i + 1 :]:
            npos = text.find(next_anchor)
            if npos != -1:
                end = npos
                break
        sections[anchor] = text[start:end]
    return sections


# ---------------------------------------------------------------------------
# 1a. Upload parsing
# ---------------------------------------------------------------------------

_LOAD_RE = re.compile(r"pd\.read_(\w+)\(([^)]+)\)")
_JSON_LOAD_RE = re.compile(r"pd\.read_json\(([^)]+)\)")


def _parse_upload(section: str) -> Optional[Dict]:
    """Extract upload entry from the 'Load data' section."""
    # Handle json_normalize wrapping: pd.json_normalize(pd.read_json(...))
    m = _JSON_LOAD_RE.search(section)
    if m and "json_normalize" in section:
        filename = _safe_literal(m.group(1))
        return {
            "action_type": "upload",
            "filename": filename,
            "file_format": "json",
        }

    m = _LOAD_RE.search(section)
    if not m:
        return None
    fmt = m.group(1)  # csv, excel, json
    filename = _safe_literal(m.group(2))
    # Normalize format names
    if fmt == "excel":
        fmt = "xlsx"
    return {
        "action_type": "upload",
        "filename": filename,
        "file_format": fmt,
    }


# ---------------------------------------------------------------------------
# 1b. Cleaning parsing
# ---------------------------------------------------------------------------

# Single-line patterns: (regex, operation key, extractor)
_SINGLE_LINE_PATTERNS = [
    # Order matters: more specific patterns first
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.lstrip\((.+?)\)"), "lstrip", True),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.lstrip\(\)"), "lstrip", False),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.rstrip\((.+?)\)"), "rstrip", True),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.rstrip\(\)"), "rstrip", False),
    (
        re.compile(
            r'df\[(.+?)\] = df\[.+?\]\.str\.replace\("\[\^a-zA-Z0-9\]"'
        ),
        "alnum",
        False,
    ),
    (re.compile(r"df = df\.dropna\(subset=\[(.+?)\]\)"), "dropna", False),
    (
        re.compile(r"df\[(.+?)\] = pd\.to_numeric\(df\[.+?\], errors='coerce'\)"),
        "to_numeric",
        False,
    ),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.astype\(str\)"), "to_string", False),
    (
        re.compile(r"df\[(.+?)\] = pd\.to_datetime\(df\[.+?\], errors='coerce'\)"),
        "to_datetime",
        False,
    ),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.lower\(\)"), "lowercase", False),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.upper\(\)"), "uppercase", False),
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.str\.strip\(\)"), "trim", False),
    (re.compile(r"df = df\.drop\(columns=\[(.+?)\]\)"), "drop_column", False),
    (re.compile(r"df = df\.drop_duplicates\(subset=\[(.+?)\]\)"), "drop_duplicates", False),
    (
        re.compile(r"df = df\.sort_values\(by=(.+?), ascending=True\)"),
        "sort_asc",
        False,
    ),
    (
        re.compile(r"df = df\.sort_values\(by=(.+?), ascending=False\)"),
        "sort_desc",
        False,
    ),
    # fillna with explicit value (single-line)
    (re.compile(r"df\[(.+?)\] = df\[.+?\]\.fillna\((.+?)\)"), "fillna", True),
    # rename_column
    (
        re.compile(r"df = df\.rename\(columns=\{(.+?): (.+?)\}\)"),
        "rename_column",
        "rename",
    ),
]


def _parse_cleaning(section: str) -> List[Dict]:
    """Parse the cleaning section into action log entries."""
    entries: List[Dict] = []
    lines = section.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        matched = False

        # Multi-line: fillna without fill_value (auto mean/mode)
        if line.startswith("if pd.api.types.is_numeric_dtype("):
            col_m = re.search(r"is_numeric_dtype\(df\[(.+?)\]\)", line)
            if col_m:
                col = _safe_literal(col_m.group(1))
                entries.append(
                    {
                        "action_type": "cleaning",
                        "operation": "fillna",
                        "column": col,
                    }
                )
                # Skip the else block (up to 3 more lines)
                i += 1
                while i < len(lines) and (
                    lines[i].strip().startswith("df[")
                    or lines[i].strip().startswith("else:")
                    or lines[i].strip() == ""
                ):
                    i += 1
                matched = True
                continue

        # Multi-line: normalize (MinMaxScaler block)
        if "pd.to_numeric" in line and i + 4 < len(lines):
            block = "\n".join(lines[i : i + 5])
            if "MinMaxScaler" in block:
                col_m = re.search(r"df\[(.+?)\]", line)
                if col_m:
                    col = _safe_literal(col_m.group(1))
                    entries.append(
                        {
                            "action_type": "cleaning",
                            "operation": "normalize",
                            "column": col,
                        }
                    )
                    i += 5
                    matched = True
                    continue

        # Multi-line: remove_outliers (zscore block)
        if "pd.to_numeric" in line and i + 4 < len(lines):
            block = "\n".join(lines[i : i + 5])
            if "zscore" in block:
                col_m = re.search(r"df\[(.+?)\]", line)
                if col_m:
                    col = _safe_literal(col_m.group(1))
                    entries.append(
                        {
                            "action_type": "cleaning",
                            "operation": "remove_outliers",
                            "column": col,
                        }
                    )
                    i += 5
                    matched = True
                    continue

        # Single-line patterns
        for pattern, op, has_extra in _SINGLE_LINE_PATTERNS:
            m = pattern.search(line)
            if m:
                if op == "rename_column":
                    col = _safe_literal(m.group(1))
                    new_name = _safe_literal(m.group(2))
                    entries.append(
                        {
                            "action_type": "cleaning",
                            "operation": "rename_column",
                            "column": col,
                            "new_name": new_name,
                        }
                    )
                elif has_extra is True:
                    col = _safe_literal(m.group(1))
                    fill_value = _safe_literal(m.group(2))
                    entries.append(
                        {
                            "action_type": "cleaning",
                            "operation": op,
                            "column": col,
                            "fill_value": fill_value,
                        }
                    )
                else:
                    col = _safe_literal(m.group(1))
                    entries.append(
                        {
                            "action_type": "cleaning",
                            "operation": op,
                            "column": col,
                        }
                    )
                matched = True
                break

        if not matched:
            # Skip unrecognized lines (imports, comments, blanks)
            pass
        i += 1

    return entries


# ---------------------------------------------------------------------------
# 1c. Chart parsing
# ---------------------------------------------------------------------------

# Extract named args from px.* calls: x=repr, y=repr, color=repr, size=repr
_PX_ARG_RE = re.compile(r"\b(x|y|color|size)=(['\"].+?['\"])")


def _parse_charts(section: str) -> List[Dict]:
    """Parse the charts section into action log entries."""
    entries: List[Dict] = []
    # Split on chart sub-anchors
    parts = _CHART_SUB_RE.split(section)
    # parts alternates: [before, chart_type, body, chart_type, body, ...]
    i = 1
    while i < len(parts) - 1:
        chart_type = parts[i].strip()
        body = parts[i + 1]

        entry: Dict = {
            "action_type": "chart",
            "chart_type": chart_type,
        }

        # Extract named args from the body
        for m in _PX_ARG_RE.finditer(body):
            arg_name = m.group(1)
            arg_value = _safe_literal(m.group(2))
            if arg_name == "x":
                entry["x_col"] = arg_value
            elif arg_name == "y":
                # Skip literal 'count' — it's a generated column, not a user column
                if arg_value != "count":
                    entry["y_col"] = arg_value
            elif arg_name == "color":
                entry["color_col"] = arg_value
            elif arg_name == "size":
                entry["size_col"] = arg_value

        entries.append(entry)
        i += 2

    return entries


# ---------------------------------------------------------------------------
# 1d. ML parsing
# ---------------------------------------------------------------------------


def _parse_ml(section: str) -> List[Dict]:
    """Parse the machine learning section into action log entries."""
    entries: List[Dict] = []
    parts = _ML_SUB_RE.split(section)
    # parts alternates: [before, task_name, body, task_name, body, ...]
    i = 1
    while i < len(parts) - 1:
        task = parts[i].strip()
        body = parts[i + 1]

        entry: Dict = {
            "action_type": "ml",
            "task": task,
        }

        # Extract feature columns from df[['x', 'y']] or df[['x']]
        cols_m = re.search(r"df\[\[(.+?)\]\]\.dropna\(\)", body)
        if cols_m:
            col_str = cols_m.group(1)
            cols = [_safe_literal(c.strip()) for c in col_str.split(",")]
            if len(cols) >= 1:
                entry["x_col"] = cols[0]
            if len(cols) >= 2:
                entry["y_col"] = cols[1]

        # Extract target column from df.loc[..., 'target']
        target_m = re.search(r"df\.loc\[.+?,\s*(.+?)\]", body)
        if target_m:
            entry["target_col"] = _safe_literal(target_m.group(1))

        # Task-specific parameters
        if task == "clustering":
            k_m = re.search(r"KMeans\(n_clusters=(\d+)", body)
            if k_m:
                entry["n_clusters"] = int(k_m.group(1))

        elif task == "classification":
            kernel_m = re.search(r"SVC\(kernel=(['\"].+?['\"])", body)
            if kernel_m:
                entry["kernel"] = _safe_literal(kernel_m.group(1))
            ts_m = re.search(r"test_size=([\d.]+)", body)
            if ts_m:
                entry["test_size"] = float(ts_m.group(1))

        elif task == "decision_tree":
            md_m = re.search(r"max_depth=(\d+)", body)
            if md_m:
                entry["max_depth"] = int(md_m.group(1))
            ts_m = re.search(r"test_size=([\d.]+)", body)
            if ts_m:
                entry["test_size"] = float(ts_m.group(1))

        elif task == "random_forest":
            ne_m = re.search(r"n_estimators=(\d+)", body)
            if ne_m:
                entry["n_estimators"] = int(ne_m.group(1))
            md_m = re.search(r"max_depth=(\d+)", body)
            if md_m:
                entry["max_depth"] = int(md_m.group(1))
            ts_m = re.search(r"test_size=([\d.]+)", body)
            if ts_m:
                entry["test_size"] = float(ts_m.group(1))

        elif task == "regression":
            ts_m = re.search(r"test_size=([\d.]+)", body)
            if ts_m:
                entry["test_size"] = float(ts_m.group(1))

        entries.append(entry)
        i += 2

    return entries


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_script(text: str) -> List[Dict]:
    """
    Parse an exported PyExploratory script back into action log entries.

    Args:
        text: The full script text (as produced by ``generate_script``).

    Returns:
        A list of action-log dicts identical in shape to those stored in
        ``actions.json``.
    """
    sections = _split_sections(text)
    entries: List[Dict] = []

    # Upload
    load_body = sections.get("# --- Load data ---", "")
    upload = _parse_upload(load_body)
    if upload:
        entries.append(upload)

    # Cleaning
    clean_body = sections.get("# --- Data cleaning ---", "")
    if clean_body:
        entries.extend(_parse_cleaning(clean_body))

    # Charts
    chart_body = sections.get("# --- Charts ---", "")
    if chart_body:
        entries.extend(_parse_charts(chart_body))

    # ML
    ml_body = sections.get("# --- Machine Learning ---", "")
    if ml_body:
        entries.extend(_parse_ml(ml_body))

    return entries
