import ollama


def ollama_localmodels() -> dict:
    localModels = ollama.list()
    print("hai")
    return [
        {"model": m.model, "parameter_size": m.details.parameter_size}
        for m in localModels.models
    ]
