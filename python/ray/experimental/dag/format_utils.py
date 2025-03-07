import ray.experimental.dag as dag


def get_indentation(num_spaces=4):
    return " " * num_spaces


def get_args_lines(bound_args):
    """Pretty prints bounded args of a DAGNode, and recursively handle
    DAGNode in list / dict containers.
    """
    indent = get_indentation()
    lines = []
    for arg in bound_args:
        if isinstance(arg, dag.DAGNode):
            node_repr_lines = str(arg).split("\n")
            for node_repr_line in node_repr_lines:
                lines.append(f"{indent}" + node_repr_line)
        elif isinstance(arg, list):
            for ele in arg:
                node_repr_lines = str(ele).split("\n")
                for node_repr_line in node_repr_lines:
                    lines.append(f"{indent}" + node_repr_line)
        elif isinstance(arg, dict):
            for _, val in arg.items():
                node_repr_lines = str(val).split("\n")
                for node_repr_line in node_repr_lines:
                    lines.append(f"{indent}" + node_repr_line)
        # TODO: (jiaodong) Handle nested containers and other obj types
        else:
            lines.append(f"{indent}" + str(arg) + ", ")

    if len(lines) == 0:
        args_line = "[]"
    else:
        args_line = "["
        for args in lines:
            args_line += f"\n{indent}{args}"
        args_line += f"\n{indent}]"

    return args_line


def get_kwargs_lines(bound_kwargs):
    """Pretty prints bounded kwargs of a DAGNode, and recursively handle
    DAGNode in list / dict containers.
    """
    indent = get_indentation()
    kwargs_lines = []
    for key, val in bound_kwargs.items():
        if isinstance(val, dag.DAGNode):
            node_repr_lines = str(val).split("\n")
            for index, node_repr_line in enumerate(node_repr_lines):
                if index == 0:
                    kwargs_lines.append(
                        f"{indent}{key}:" + f"{indent}" + node_repr_line
                    )
                else:
                    kwargs_lines.append(f"{indent}{indent}" + node_repr_line)

        elif isinstance(val, list):
            for ele in val:
                node_repr_lines = str(ele).split("\n")
                for node_repr_line in node_repr_lines:
                    kwargs_lines.append(f"{indent}" + node_repr_line)
        elif isinstance(val, dict):
            for _, inner_val in val.items():
                node_repr_lines = str(inner_val).split("\n")
                for node_repr_line in node_repr_lines:
                    kwargs_lines.append(f"{indent}" + node_repr_line)
        # TODO: (jiaodong) Handle nested containers and other obj types
        else:
            kwargs_lines.append(val)

    if len(kwargs_lines) > 0:
        kwargs_line = "{"
        for line in kwargs_lines:
            kwargs_line += f"\n{indent}{line}"
        kwargs_line += f"\n{indent}}}"
    else:
        kwargs_line = "{}"

    return kwargs_line


def get_options_lines(bound_options):
    """Pretty prints .options() in DAGNode. Only prints non-empty values."""
    if not bound_options:
        return "{}"
    indent = get_indentation()
    options_lines = []
    for key, val in bound_options.items():
        if val:
            options_lines.append(f"{indent}{key}: " + str(val))

    options_line = "{"
    for line in options_lines:
        options_line += f"\n{indent}{line}"
    options_line += f"\n{indent}}}"
    return options_line
