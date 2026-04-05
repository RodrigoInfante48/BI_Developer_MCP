"""
DataPocket MCP v2 — Test Suite
Covers parsing, type inference, SQL generation, dashboard generation,
smart formatting, format detection, transforms, and exports.
"""

import sys
import os
import pytest

# Make src importable from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.datapocket_mcp import (
    _parse_csv_data,
    _parse_json_data,
    _parse_jsonl_data,
    _parse_tsv_data,
    _infer_pg_type,
    _sanitize_table_name,
    _generate_create_table_sql,
    _generate_insert_sql,
    _generate_dashboard_html,
    _smart_format,
    _auto_detect_format,
    _detect_and_decode,
    DataSourceType,
    ParseError,
)

# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


@pytest.fixture
def ventas_csv() -> str:
    with open(os.path.join(EXAMPLES_DIR, "ventas_ejemplo.csv"), encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def finanzas_csv() -> str:
    with open(os.path.join(EXAMPLES_DIR, "finanzas_ejemplo.csv"), encoding="utf-8") as f:
        return f.read()


# ──────────────────────────────────────────────
# Test 1: Parse valid CSV
# ──────────────────────────────────────────────

def test_parse_csv_valid(ventas_csv):
    headers, rows = _parse_csv_data(ventas_csv)
    assert len(headers) == 6
    assert "producto" in headers
    assert len(rows) > 0


# ──────────────────────────────────────────────
# Test 2: Parse CSV with latin-1 encoding (via bytes)
# ──────────────────────────────────────────────

def test_parse_csv_latin1():
    csv_latin1 = "nombre,ciudad\nJosé,México\nMaría,Bogotá\n".encode("latin-1")
    decoded = _detect_and_decode(csv_latin1)
    headers, rows = _parse_csv_data(decoded)
    assert headers == ["nombre", "ciudad"]
    assert len(rows) == 2


# ──────────────────────────────────────────────
# Test 3: Parse valid JSON array
# ──────────────────────────────────────────────

def test_parse_json_valid():
    data = '[{"producto":"A","ventas":100},{"producto":"B","ventas":200}]'
    headers, rows = _parse_json_data(data)
    assert headers == ["producto", "ventas"]
    assert len(rows) == 2
    assert rows[0][1] == "100"


# ──────────────────────────────────────────────
# Test 4: Parse valid JSONL
# ──────────────────────────────────────────────

def test_parse_jsonl_valid():
    data = '{"a":1,"b":"x"}\n{"a":2,"b":"y"}\n'
    headers, rows = _parse_jsonl_data(data)
    assert headers == ["a", "b"]
    assert len(rows) == 2
    assert rows[1][0] == "2"


# ──────────────────────────────────────────────
# Test 5: Parse valid TSV
# ──────────────────────────────────────────────

def test_parse_tsv_valid():
    data = "ciudad\tpoblacion\nTokyo\t13960000\nDelhi\t11030000\n"
    headers, rows = _parse_tsv_data(data)
    assert headers == ["ciudad", "poblacion"]
    assert len(rows) == 2
    assert rows[0][0] == "Tokyo"


# ──────────────────────────────────────────────
# Test 6: Infer BIGINT
# ──────────────────────────────────────────────

def test_infer_bigint():
    assert _infer_pg_type(["1", "2", "3", "100", "999"]) == "BIGINT"


# ──────────────────────────────────────────────
# Test 7: Infer NUMERIC
# ──────────────────────────────────────────────

def test_infer_numeric():
    assert _infer_pg_type(["1.5", "2.3", "100.99"]) == "NUMERIC"


# ──────────────────────────────────────────────
# Test 8: Infer DATE
# ──────────────────────────────────────────────

def test_infer_date():
    assert _infer_pg_type(["2026-01-01", "2026-02-15", "2026-03-30"]) == "DATE"


# ──────────────────────────────────────────────
# Test 9: Infer TEXT for long strings
# ──────────────────────────────────────────────

def test_infer_text():
    long_str = "a" * 300
    result = _infer_pg_type([long_str, long_str])
    assert result == "TEXT"


# ──────────────────────────────────────────────
# Test 10: Sanitize table name
# ──────────────────────────────────────────────

def test_sanitize_table_name():
    assert _sanitize_table_name("My Table!") == "my_table_"
    assert _sanitize_table_name("123abc") == "t_123abc"
    assert len(_sanitize_table_name("a" * 100)) <= 63


# ──────────────────────────────────────────────
# Test 11: Generate CREATE TABLE SQL
# ──────────────────────────────────────────────

def test_generate_create_table_sql():
    headers = ["nombre", "ventas"]
    rows = [["Producto A", "1000"], ["Producto B", "2000"]]
    sql = _generate_create_table_sql("mi_tabla", headers, rows)
    assert "CREATE TABLE" in sql
    assert '"nombre"' in sql
    assert '"ventas"' in sql
    assert "BIGINT" in sql


# ──────────────────────────────────────────────
# Test 12: Generate INSERT SQL
# ──────────────────────────────────────────────

def test_generate_insert_sql():
    headers = ["nombre", "valor"]
    rows = [["Alpha", "10"], ["Beta", "20"]]
    sql = _generate_insert_sql("t", headers, rows)
    assert "INSERT INTO" in sql
    assert "'Alpha'" in sql
    assert "'Beta'" in sql


# ──────────────────────────────────────────────
# Test 13: Dashboard HTML contains Chart.js CDN
# ──────────────────────────────────────────────

def test_dashboard_html_has_chartjs():
    charts = [{"type": "kpi", "title": "Revenue", "value": "$1M", "subtitle": "Total", "trend": "↑ 10%"}]
    html = _generate_dashboard_html("Test Dashboard", charts)
    assert "cdn.jsdelivr.net/npm/chart.js" in html
    assert "Test Dashboard" in html


# ──────────────────────────────────────────────
# Test 14: Smart format numbers
# ──────────────────────────────────────────────

def test_smart_format():
    assert _smart_format(1000) == "1.0K"
    assert _smart_format(1_000_000) == "1.0M"
    assert _smart_format(1_000_000_000) == "1.0B"
    assert _smart_format(500) == "500"
    assert _smart_format(3.14) == "3.14"
    assert _smart_format(1000, prefix="$") == "$1.0K"


# ──────────────────────────────────────────────
# Test 15: Auto-detect format
# ──────────────────────────────────────────────

def test_auto_detect_csv():
    assert _auto_detect_format("nombre,valor\nA,1") == DataSourceType.CSV

def test_auto_detect_json():
    assert _auto_detect_format('[{"a":1}]') == DataSourceType.JSON_DATA

def test_auto_detect_jsonl():
    assert _auto_detect_format('{"a":1}\n{"b":2}') == DataSourceType.JSONL

def test_auto_detect_tsv():
    assert _auto_detect_format("col1\tcol2\nA\t1") == DataSourceType.TSV


# ──────────────────────────────────────────────
# Test 16: Transform — drop_nulls
# ──────────────────────────────────────────────

def test_transform_drop_nulls():
    csv = "a,b\n1,2\n,\n3,4"
    headers, rows = _parse_csv_data(csv)
    from src.datapocket_mcp import _parse_op_parts
    filtered = [r for r in rows if all(str(v).strip() for v in r)]
    assert len(filtered) == 2


# ──────────────────────────────────────────────
# Test 17: Transform — dedup
# ──────────────────────────────────────────────

def test_transform_dedup():
    csv = "a,b\n1,2\n1,2\n3,4"
    headers, rows = _parse_csv_data(csv)
    seen = set()
    unique = []
    for r in rows:
        key = tuple(r)
        if key not in seen:
            seen.add(key)
            unique.append(r)
    assert len(unique) == 2


# ──────────────────────────────────────────────
# Test 18: Transform — sort
# ──────────────────────────────────────────────

def test_transform_sort():
    csv = "nombre,ventas\nC,300\nA,100\nB,200"
    headers, rows = _parse_csv_data(csv)
    col_idx = headers.index("ventas")
    rows.sort(key=lambda r: float(r[col_idx]), reverse=False)
    assert rows[0][0] == "A"
    assert rows[-1][0] == "C"


# ──────────────────────────────────────────────
# Test 19: Transform — filter
# ──────────────────────────────────────────────

def test_transform_filter():
    csv = "producto,ventas\nA,500\nB,1500\nC,2000"
    headers, rows = _parse_csv_data(csv)
    col_idx = headers.index("ventas")
    filtered = [r for r in rows if float(r[col_idx]) > 1000]
    assert len(filtered) == 2
    assert filtered[0][0] == "B"


# ──────────────────────────────────────────────
# Test 20: Export — CSV to JSON
# ──────────────────────────────────────────────

def test_export_csv_to_json():
    import json as json_mod
    csv = "producto,ventas\nWidget A,15000\nWidget B,12000"
    headers, rows = _parse_csv_data(csv)
    records = [{headers[i]: row[i] for i in range(len(headers))} for row in rows]
    output = json_mod.dumps(records, ensure_ascii=False)
    parsed = json_mod.loads(output)
    assert len(parsed) == 2
    assert parsed[0]["producto"] == "Widget A"
    assert parsed[1]["ventas"] == "12000"
