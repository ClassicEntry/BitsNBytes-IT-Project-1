"""
Translate an action log into a standalone Python script.

The generated ``.py`` file uses only standard data-science libraries
(pandas, plotly, scikit-learn) — no pyexploratory imports.
"""

from typing import Dict, List, Set


# ---------------------------------------------------------------------------
# Cleaning operation → raw pandas code
# ---------------------------------------------------------------------------

def _cleaning_code(entry: Dict) -> str:
    """Return one or more lines of pandas code for a cleaning operation."""
    col = repr(entry["column"])
    op = entry["operation"]
    fv = entry.get("fill_value")
    new_name = entry.get("new_name")

    mapping = {
        "lstrip": (
            f"df[{col}] = df[{col}].str.lstrip({repr(fv)})"
            if fv else f"df[{col}] = df[{col}].str.lstrip()"
        ),
        "rstrip": (
            f"df[{col}] = df[{col}].str.rstrip({repr(fv)})"
            if fv else f"df[{col}] = df[{col}].str.rstrip()"
        ),
        "alnum": f'df[{col}] = df[{col}].str.replace("[^a-zA-Z0-9]", "", regex=True)',
        "dropna": f"df = df.dropna(subset=[{col}])",
        "to_numeric": f"df[{col}] = pd.to_numeric(df[{col}], errors='coerce')",
        "to_string": f"df[{col}] = df[{col}].astype(str)",
        "to_datetime": f"df[{col}] = pd.to_datetime(df[{col}], errors='coerce')",
        "lowercase": f"df[{col}] = df[{col}].str.lower()",
        "uppercase": f"df[{col}] = df[{col}].str.upper()",
        "trim": f"df[{col}] = df[{col}].str.strip()",
        "drop_column": f"df = df.drop(columns=[{col}])",
        "drop_duplicates": f"df = df.drop_duplicates(subset=[{col}])",
        "sort_asc": f"df = df.sort_values(by={col}, ascending=True)",
        "sort_desc": f"df = df.sort_values(by={col}, ascending=False)",
    }

    if op in mapping:
        return mapping[op]

    if op == "fillna":
        if fv is not None:
            return f"df[{col}] = df[{col}].fillna({repr(fv)})"
        # Match app behavior: mean for numeric, mode for non-numeric
        return (
            f"if pd.api.types.is_numeric_dtype(df[{col}]):\n"
            f"    df[{col}] = df[{col}].fillna(df[{col}].mean())\n"
            f"else:\n"
            f"    df[{col}] = df[{col}].fillna(df[{col}].mode()[0])"
        )

    if op == "rename_column":
        if new_name:
            return f"df = df.rename(columns={{{col}: {repr(new_name)}}})"
        return f"# rename_column on {col} (no new name provided — skipped)"

    if op == "normalize":
        return (
            f"df[{col}] = pd.to_numeric(df[{col}], errors='coerce')\n"
            f"df[{col}] = df[{col}].fillna(0)\n"
            f"from sklearn.preprocessing import MinMaxScaler\n"
            f"_scaler = MinMaxScaler()\n"
            f"df[{col}] = _scaler.fit_transform(df[[{col}]])"
        )

    if op == "remove_outliers":
        return (
            f"df[{col}] = pd.to_numeric(df[{col}], errors='coerce')\n"
            f"_z = np.abs(scipy.stats.zscore(df[{col}].dropna()))\n"
            f"_mask = df[{col}].notna()\n"
            f"_mask.loc[df[{col}].notna()] = _z >= 3\n"
            f"df.loc[_mask, {col}] = None"
        )

    return f"# Unknown cleaning operation: {op}"


# ---------------------------------------------------------------------------
# Chart → plotly code
# ---------------------------------------------------------------------------

def _chart_code(entry: Dict) -> str:
    """Return plotly code for a chart action."""
    ct = entry["chart_type"]
    x = repr(entry.get("x_col")) if entry.get("x_col") else "None"
    y = repr(entry.get("y_col")) if entry.get("y_col") else "None"
    color = repr(entry.get("color_col")) if entry.get("color_col") else "None"
    size = repr(entry.get("size_col")) if entry.get("size_col") else "None"

    lines = [f"\n# --- Chart: {ct} ---"]

    if ct == "histogram":
        c = f", color={color}" if entry.get("color_col") else ""
        lines.append(f"fig = px.histogram(df, x={x}{c}, title=f'Histogram of {{{x}}}')")
    elif ct == "boxplot":
        c = f", color={color}" if entry.get("color_col") else ""
        lines.append(f"fig = px.box(df, y={x}{c}, title=f'Box Plot of {{{x}}}')")
    elif ct == "scatter":
        c = f", color={color}" if entry.get("color_col") else ""
        lines.append(f"fig = px.scatter(df, x={x}, y={y}{c}, title=f'{{{x}}} vs {{{y}}}')")
    elif ct == "line":
        lines.append(f"fig = px.line(df, x={x}, y={y}, title=f'Line: {{{x}}} vs {{{y}}}')")
    elif ct == "bar":
        lines.append(f"# Bar chart — value counts of column")
        lines.append(f"_counts = df[{x}].value_counts().reset_index()")
        lines.append(f"_counts.columns = [{x}, 'count']")
        lines.append(f"fig = px.bar(_counts, x={x}, y='count', title=f'Distribution of {{{x}}}')")
    elif ct == "pie":
        lines.append(f"fig = px.pie(df, names={x}, title=f'Pie Chart of {{{x}}}')")
    elif ct == "area":
        c = f", color={color}" if entry.get("color_col") else ""
        lines.append(f"fig = px.area(df, x={x}, y={y}{c}, title=f'Area: {{{x}}} vs {{{y}}}')")
    elif ct == "violin":
        lines.append(f"fig = px.violin(df, x={x}, y={y}, box=True, title=f'Violin: {{{y}}} by {{{x}}}')")
    elif ct == "heatmap":
        lines.append("_num = df.select_dtypes('number')")
        lines.append("_corr = _num.corr()")
        lines.append("fig = go.Figure(go.Heatmap(z=_corr.values, x=_corr.columns.tolist(), "
                      "y=_corr.columns.tolist(), colorscale='RdBu_r', zmin=-1, zmax=1, "
                      "text=np.round(_corr.values, 2), texttemplate='%{text}'))")
        lines.append("fig.update_layout(title='Correlation Heatmap')")
    elif ct == "pairplot":
        c = f", color={color}" if entry.get("color_col") else ""
        lines.append(f"_cols = df.select_dtypes('number').columns.tolist()[:6]")
        lines.append(f"fig = px.scatter_matrix(df, dimensions=_cols{c}, title='Pair Plot')")
        lines.append("fig.update_traces(diagonal_visible=True, marker=dict(size=3))")
        lines.append("fig.update_layout(height=700)")
    elif ct == "correlation":
        lines.append("_num = df.select_dtypes('number')")
        lines.append("_corr = _num.corr()")
        lines.append("fig = go.Figure(go.Heatmap(z=_corr.values, x=_corr.columns.tolist(), "
                      "y=_corr.columns.tolist(), colorscale='Viridis', "
                      "text=np.round(_corr.values, 3), texttemplate='%{text}'))")
        lines.append("fig.update_layout(title='Correlation Matrix')")
    elif ct == "bubble":
        c = f", color={color}" if entry.get("color_col") else ""
        s = f", size={size}" if entry.get("size_col") else ""
        lines.append(f"fig = px.scatter(df, x={x}, y={y}{c}{s}, title=f'Bubble: {{{x}}} vs {{{y}}}')")
    elif ct == "treemap":
        lines.append(f"_counts = df[{x}].value_counts().reset_index()")
        lines.append(f"_counts.columns = [{x}, 'count']")
        lines.append(f"fig = px.treemap(_counts, path=[{x}], values='count', title=f'Treemap: {{{x}}}')")
    elif ct == "sunburst":
        lines.append(f"_counts = df[{x}].value_counts().reset_index()")
        lines.append(f"_counts.columns = [{x}, 'count']")
        lines.append(f"fig = px.sunburst(_counts, path=[{x}], values='count', title=f'Sunburst: {{{x}}}')")
    else:
        lines.append(f"# Unknown chart type: {ct}")
        return "\n".join(lines)

    lines.append("fig.show()")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ML task → scikit-learn code
# ---------------------------------------------------------------------------

def _ml_code(entry: Dict) -> str:
    """Return scikit-learn code for an ML action."""
    task = entry["task"]
    lines = [f"\n# --- ML: {task} ---"]

    if task == "clustering":
        x = repr(entry["x_col"])
        y = repr(entry["y_col"])
        k = entry.get("n_clusters", 3)
        lines += [
            f"from sklearn.cluster import KMeans",
            f"from sklearn.preprocessing import StandardScaler",
            f"from sklearn.metrics import silhouette_score",
            f"_X = df[[{x}, {y}]].dropna()",
            f"_X_scaled = StandardScaler().fit_transform(_X)",
            f"_km = KMeans(n_clusters={k}, random_state=42, n_init='auto')",
            f"_labels = _km.fit_predict(_X_scaled)",
            f"print(f'Silhouette Score: {{silhouette_score(_X_scaled, _labels):.3f}}')",
        ]
    elif task == "classification":
        x = repr(entry["x_col"])
        y = repr(entry["y_col"])
        target = repr(entry["target_col"])
        kernel = repr(entry.get("kernel", "linear"))
        ts = entry.get("test_size", 0.25)
        lines += [
            f"from sklearn.svm import SVC",
            f"from sklearn.model_selection import train_test_split",
            f"from sklearn.preprocessing import StandardScaler, LabelEncoder",
            f"from sklearn.metrics import classification_report, accuracy_score",
            f"_X = df[[{x}, {y}]].dropna()",
            f"_y = LabelEncoder().fit_transform(df.loc[_X.index, {target}])",
            f"_X_scaled = StandardScaler().fit_transform(_X)",
            f"_X_train, _X_test, _y_train, _y_test = train_test_split(_X_scaled, _y, test_size={ts}, random_state=42)",
            f"_clf = SVC(kernel={kernel}, random_state=42)",
            f"_clf.fit(_X_train, _y_train)",
            f"_y_pred = _clf.predict(_X_test)",
            f"print(classification_report(_y_test, _y_pred))",
            f"print(f'Accuracy: {{accuracy_score(_y_test, _y_pred):.3f}}')",
        ]
    elif task == "decision_tree":
        x = repr(entry["x_col"])
        y = repr(entry["y_col"])
        target = repr(entry["target_col"])
        md = entry.get("max_depth", 5)
        ts = entry.get("test_size", 0.25)
        lines += [
            f"from sklearn.tree import DecisionTreeClassifier",
            f"from sklearn.model_selection import train_test_split",
            f"from sklearn.preprocessing import StandardScaler, LabelEncoder",
            f"from sklearn.metrics import classification_report, accuracy_score",
            f"_X = df[[{x}, {y}]].dropna()",
            f"_y = LabelEncoder().fit_transform(df.loc[_X.index, {target}])",
            f"_X_scaled = StandardScaler().fit_transform(_X)",
            f"_X_train, _X_test, _y_train, _y_test = train_test_split(_X_scaled, _y, test_size={ts}, random_state=42)",
            f"_clf = DecisionTreeClassifier(max_depth={md}, random_state=42)",
            f"_clf.fit(_X_train, _y_train)",
            f"_y_pred = _clf.predict(_X_test)",
            f"print(classification_report(_y_test, _y_pred))",
            f"print(f'Accuracy: {{accuracy_score(_y_test, _y_pred):.3f}}')",
        ]
    elif task == "random_forest":
        x = repr(entry["x_col"])
        y = repr(entry["y_col"])
        target = repr(entry["target_col"])
        ne = entry.get("n_estimators", 100)
        md = entry.get("max_depth", 5)
        ts = entry.get("test_size", 0.25)
        lines += [
            f"from sklearn.ensemble import RandomForestClassifier",
            f"from sklearn.model_selection import train_test_split",
            f"from sklearn.preprocessing import StandardScaler, LabelEncoder",
            f"from sklearn.metrics import classification_report, accuracy_score",
            f"_X = df[[{x}, {y}]].dropna()",
            f"_y = LabelEncoder().fit_transform(df.loc[_X.index, {target}])",
            f"_X_scaled = StandardScaler().fit_transform(_X)",
            f"_X_train, _X_test, _y_train, _y_test = train_test_split(_X_scaled, _y, test_size={ts}, random_state=42)",
            f"_clf = RandomForestClassifier(n_estimators={ne}, max_depth={md}, random_state=42)",
            f"_clf.fit(_X_train, _y_train)",
            f"_y_pred = _clf.predict(_X_test)",
            f"print(classification_report(_y_test, _y_pred))",
            f"print(f'Accuracy: {{accuracy_score(_y_test, _y_pred):.3f}}')",
        ]
    elif task == "regression":
        x = repr(entry["x_col"])
        target = repr(entry["target_col"])
        ts = entry.get("test_size", 0.25)
        lines += [
            f"from sklearn.linear_model import LinearRegression",
            f"from sklearn.model_selection import train_test_split",
            f"from sklearn.metrics import mean_squared_error, r2_score",
            f"_X = df[[{x}]].dropna()",
            f"_y = df.loc[_X.index, {target}]",
            f"_X_train, _X_test, _y_train, _y_test = train_test_split(_X, _y, test_size={ts}, random_state=42)",
            f"_reg = LinearRegression()",
            f"_reg.fit(_X_train, _y_train)",
            f"_y_pred = _reg.predict(_X_test)",
            f"print(f'R-squared: {{r2_score(_y_test, _y_pred):.4f}}')",
            f"print(f'MSE: {{mean_squared_error(_y_test, _y_pred):.4f}}')",
        ]
    else:
        lines.append(f"# Unknown ML task: {task}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Import collector
# ---------------------------------------------------------------------------

def _collect_imports(log: List[Dict]) -> str:
    """Scan the log to determine which libraries are needed."""
    needs_plotly_express = False
    needs_plotly_go = False
    needs_numpy = False
    needs_scipy = False

    for entry in log:
        at = entry.get("action_type")
        if at == "chart":
            ct = entry.get("chart_type", "")
            if ct in ("heatmap", "correlation"):
                needs_plotly_go = True
                needs_numpy = True
            else:
                needs_plotly_express = True
            if ct == "pairplot":
                needs_plotly_express = True
        if at == "cleaning" and entry.get("operation") == "remove_outliers":
            needs_numpy = True
            needs_scipy = True

    lines = ["import pandas as pd"]
    if needs_numpy:
        lines.append("import numpy as np")
    if needs_scipy:
        lines.append("import scipy.stats")
    if needs_plotly_express:
        lines.append("import plotly.express as px")
    if needs_plotly_go:
        lines.append("import plotly.graph_objects as go")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_script(action_log: List[Dict]) -> str:
    """Convert an action log into a standalone Python script string."""
    # Filter out disabled steps before generating
    action_log = [e for e in action_log if not e.get("disabled", False)]

    if not action_log:
        return (
            '"""PyExploratory session — no actions recorded."""\n\n'
            "print('No actions were recorded in this session.')\n"
        )

    sections: List[str] = []

    # Docstring
    sections.append('"""')
    sections.append("PyExploratory — exported session script.")
    sections.append("Generated automatically. Run with: python pyexploratory_session.py")
    sections.append('"""')

    # Imports
    sections.append("")
    sections.append(_collect_imports(action_log))

    # Data loading
    upload = next((e for e in action_log if e["action_type"] == "upload"), None)
    if upload:
        fname = repr(upload["filename"])
        fmt = upload.get("file_format", "csv")
        sections.append("")
        sections.append("# --- Load data ---")
        if fmt == "csv":
            sections.append(f"df = pd.read_csv({fname})")
        elif fmt in ("xls", "xlsx"):
            sections.append(f"df = pd.read_excel({fname})")
        elif fmt == "json":
            sections.append(f"df = pd.json_normalize(pd.read_json({fname}).to_dict(orient='records'))")
        else:
            sections.append(f"df = pd.read_csv({fname})  # format: {fmt}")

    # Cleaning
    cleaning_entries = [e for e in action_log if e["action_type"] == "cleaning"]
    if cleaning_entries:
        sections.append("")
        sections.append("# --- Data cleaning ---")
        for entry in cleaning_entries:
            sections.append(_cleaning_code(entry))

    # Charts
    chart_entries = [e for e in action_log if e["action_type"] == "chart"]
    if chart_entries:
        sections.append("")
        sections.append("# --- Charts ---")
        for entry in chart_entries:
            sections.append(_chart_code(entry))

    # ML
    ml_entries = [e for e in action_log if e["action_type"] == "ml"]
    if ml_entries:
        sections.append("")
        sections.append("# --- Machine Learning ---")
        for entry in ml_entries:
            sections.append(_ml_code(entry))

    sections.append("")
    return "\n".join(sections)
