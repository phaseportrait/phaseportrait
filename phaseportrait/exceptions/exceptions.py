class PortraitExceptions(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class dFNotCallable(PortraitExceptions):
    def __init__(self, func):
        super().__init__(f"The object {func} is not a callable function")

class dFInvalid(PortraitExceptions):
    def __init__(self, sig, dF_args):
        super().__init__(f"`dF` function has {len(sig.parameters)} arguments, {2+len(dF_args)} were given")

class dF_argsInvalid(PortraitExceptions):
    def __init__(self, dF_args):
        super().__init__(f"The object `dF_args={dF_args}` must be a dictionary, not {type(dF_args)} type")

class InvalidRange(PortraitExceptions):
    def __init__(self, text):
        super().__init__(f"Invalid range: {text}")

class dFArgsRequired(PortraitExceptions):
    def __init__(self):
        super().__init__(f"When keyword numba=True a dictionary must be necessarily passed to keyword dF_args containing additional parameters of given dF function")