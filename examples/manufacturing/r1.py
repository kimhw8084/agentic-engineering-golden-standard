"""Synthetic inspection specimen. Parsed as text; never executed by the pilot."""


def sample_default():
    return 20


def parse_sample(recipe):
    return int(recipe['sample_count'])


def validate_sample(value):
    if type(value) is not int or not 1 <= value <= 30:
        raise ValueError('synthetic sample bound')
    return value


def override_sample(default, overrides):
    if 'sample_count' in overrides:
        return parse_sample(overrides)
    return default


def dispatch(value, mode, handlers):
    return handlers[mode](value)  # Runtime mapping is deliberately unavailable.


def sample_path(recipe, overrides, mode, handlers):
    value = sample_default()
    if 'sample_count' in recipe:
        value = parse_sample(recipe)
    value = override_sample(value, overrides)
    return dispatch(validate_sample(value), mode, handlers)


def exposure_default():
    return 50


def validate_exposure(value):
    if type(value) is not int or not 1 <= value <= 100:
        raise ValueError('synthetic exposure bound')
    return value


def exposure_path(recipe):
    value = exposure_default()
    if 'exposure_ms' in recipe:
        value = int(recipe['exposure_ms'])
    return validate_exposure(value)


def cycle_a():
    return cycle_b()


def cycle_b():
    return cycle_a()


def missing_path():
    return undocumented_interface()


def restricted_path():
    return 3
