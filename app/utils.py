from uuid import uuid4


def new_uuid() -> str:
    return str(uuid4())


def business_errors_to_swagger(*args) -> dict:
    responses = dict()

    error_codes = dict()

    errors = []

    for arg in args:
        error_codes[arg.status_code] = []
        errors.append(arg())

    for error in errors:
        error_codes[error.status_code].append(error.to_dict())

    for error in errors:
        examples = error_codes[error.status_code]
        example = examples if len(examples) > 1 else examples[0]
        responses[error.status_code] = dict(content={"application/json": {"example": example}})

    return responses
