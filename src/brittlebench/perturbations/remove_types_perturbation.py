"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re
import ast

from brittlebench.perturbations.perturbation import TextPerturbation

class Remover(ast.NodeTransformer):
    """
    AST NodeTransformer that removes type annotations from function definitions and variable annotations.
    """
    def visit_FunctionDef(self, node):  # type: ignore[override]
        # Remove return annotation
        node.returns = None
        # Remove parameter annotations
        self.strip_args(node.args)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):  # type: ignore[override]
        node.returns = None
        self.strip_args(node.args)
        self.generic_visit(node)
        return node

    def strip_args(self, args):
        for a in getattr(args, 'posonlyargs', []):
            a.annotation = None
        for a in args.args:
            a.annotation = None
        for a in args.kwonlyargs:
            a.annotation = None
        if args.vararg:
            args.vararg.annotation = None
        if args.kwarg:
            args.kwarg.annotation = None

    def visit_AnnAssign(self, node):  # type: ignore[override]
        # If there is a value turn into a simple Assign, else drop
        if node.value is None:
            return None
        new = ast.Assign(targets=[node.target], value=node.value)
        return ast.copy_location(new, node)


class RemoveTypesPerturbation(TextPerturbation):
    """A perturbation that removes type annotations from code snippets."""

    @staticmethod
    def _remove_types_ast(code: str) -> str:
        """Attempt to remove annotations using AST. This runs for valid Python code only."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            raise

        new_tree = Remover().visit(tree)
        ast.fix_missing_locations(new_tree)
        try:
            return ast.unparse(new_tree)
        except Exception:
            # Fallback – should rarely happen
            return code

    @staticmethod
    def _split_params_top_level(params: str) -> list[str]:
        """Split parameter string into segments at top-level commas."""
        segs = []
        depth_paren = 0
        depth_brack = 0
        depth_brace = 0
        current = []
        for ch in params:
            if ch == ',' and depth_paren == depth_brack == depth_brace == 0:
                seg = ''.join(current).strip()
                if seg:
                    segs.append(seg)
                current = []
            else:
                current.append(ch)
                if ch == '(': depth_paren += 1
                elif ch == ')': depth_paren -= 1 if depth_paren else 0
                elif ch == '[': depth_brack += 1
                elif ch == ']': depth_brack -= 1 if depth_brack else 0
                elif ch == '{': depth_brace += 1
                elif ch == '}': depth_brace -= 1 if depth_brace else 0
        last = ''.join(current).strip()
        if last:
            segs.append(last)
        return segs

    @staticmethod
    def _strip_param_annotation(segment: str) -> str:
        """Strip type annotation from a single parameter segment."""
        seg = segment.strip()
        trailing_comma = False
        if seg.endswith(','):
            trailing_comma = True
            seg = seg[:-1]

        prefix = ''
        if seg.startswith('**'):
            prefix = '**'
            seg = seg[2:]
        elif seg.startswith('*'):
            prefix = '*'
            seg = seg[1:]

        default_part = ''
        if '=' in seg:
            left, right = seg.split('=', 1)
            default_part = '=' + right.strip()
        else:
            left = seg

        # Remove first colon outside any bracket nesting
        stripped_left = []
        depth_paren = depth_brack = depth_brace = 0
        colon_removed = False
        for ch in left:
            if ch == ':' and depth_paren == depth_brack == depth_brace == 0 and not colon_removed:
                colon_removed = True
                break  # discard rest (the annotation)
            else:
                stripped_left.append(ch)
                if ch == '(': depth_paren += 1
                elif ch == ')': depth_paren -= 1 if depth_paren else 0
                elif ch == '[': depth_brack += 1
                elif ch == ']': depth_brack -= 1 if depth_brack else 0
                elif ch == '{': depth_brace += 1
                elif ch == '}': depth_brace -= 1 if depth_brace else 0
        name_part = ''.join(stripped_left).strip()
        rebuilt = f"{prefix}{name_part}{(' ' + default_part) if default_part else ''}".rstrip()
        if trailing_comma:
            rebuilt += ','
        return rebuilt

    def _heuristic_remove_types(self, code: str) -> str:
        lines = code.split('\n')
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('def '):
                # Accumulate signature lines until ':' with balanced parens
                sig_lines = [line]
                paren_balance = line.count('(') - line.count(')')
                j = i + 1
                while j < len(lines) and paren_balance > 0:
                    sig_lines.append(lines[j])
                    paren_balance += lines[j].count('(') - lines[j].count(')')
                    j += 1
                signature = '\n'.join(sig_lines)
                # Process return annotation
                signature = re.sub(r"\)\s*->\s*[^:]+:", "):", signature)
                # If single line
                if len(sig_lines) == 1:
                    m = re.search(r"def[^()]*\((.*)\):", signature)
                    if m:
                        params = m.group(1)
                        cleaned = ", ".join(self._strip_param_annotation(p) for p in self._split_params_top_level(params))
                        signature = re.sub(r"\((.*)\):", f"({cleaned}):", signature)
                    out.append(signature)
                else:
                    # Multi-line case: process each param line except first & last if they hold closing paren
                    processed = []
                    for k, sl in enumerate(sig_lines):
                        if k == 0:
                            processed.append(sl)
                            continue
                        if k == len(sig_lines) - 1 and sl.strip().startswith(')'):
                            # Closing line
                            closing = re.sub(r"\)\s*->\s*[^:]+:", "):", sl)
                            processed.append(closing)
                            continue
                        # Parameter line
                        stripped = self._strip_param_annotation(sl)
                        processed.append(stripped)
                    out.extend(processed)
                i = j
                continue
            # Variable annotation with assignment
            var_assign = re.match(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([^=]+?)\s*=\s*(.+)$", line)
            if var_assign:
                indent, name, _, value = var_assign.groups()
                out.append(f"{indent}{name} = {value}")
                i += 1
                continue
            # Standalone annotation – drop line
            if re.match(r"^\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*.+$", line):
                i += 1
                continue
            out.append(line)
            i += 1
        return '\n'.join(out)

    def _remove_type_hints(self, code: str) -> str:
        """Remove type hints (parameters, returns, variable annotations) from a code snippet.

        Tries AST removal first and if the code is not valid Python, falls back to
        heuristic line-based removal to preserve as much of the original layout as possible.
        """
        if not code:
            return code
        try:
            return self._remove_types_ast(code)
        except SyntaxError:
            print('Warning: Code is not valid Python, falling back to heuristic type removal.')
            return self._heuristic_remove_types(code)


    def apply(self, text: str) -> str:  # type: ignore[override]
        return self._remove_type_hints(text)