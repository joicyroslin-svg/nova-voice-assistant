from __future__ import annotations

import ast
import operator


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return float(OPS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _eval_node(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("Unsupported expression")


def calculate_expression(expr: str) -> str:
    safe_expr = expr.strip().replace("^", "**")
    try:
        tree = ast.parse(safe_expr, mode="eval")
        result = _eval_node(tree.body)
        return f"The result is {result:g}"
    except Exception:
        return "I could not calculate that. Try something like calculate 12 / 4 + 3."
