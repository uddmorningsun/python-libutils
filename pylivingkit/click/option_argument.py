import typing

import click


def extend_option_withattrs(opt: click.Option, attrs: typing.Dict[str, typing.Any]) -> click.Option:
    """Extend click.Option extra attributes for defining click.Command.params or f.__click_params__
    from click.decorators:_param_memo.

    1) click.Command.params.append(extend_option_withattrs(click.Option(), {"prompt": "New Prompt Message"})
    2) f.__click_params__.append(extend_option_withattrs(click.Option(), {"prompt": "New Prompt Message"})
    """
    for key, value in attrs.items():
        setattr(opt, key, value)
    return opt
