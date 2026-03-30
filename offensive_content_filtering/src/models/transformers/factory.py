from .hugging_face_model import HuggingFaceModel
from .detoxify_model import DetoxifyModel
from .tokenizers import HuggingFaceTokenizer, DetoxifyTokenizer


def build_transformer_model(model_type: str, **kwargs):
    """
    Factory for transformer models + tokenizers.

    Args:
        model_type (str): "huggingface" or "detoxify"
        **kwargs: model-specific arguments

    Returns:
        (model, tokenizer)
    """

    if model_type == "huggingface":
        model_name = kwargs.get("model_name")
        model_path = kwargs.get("model_path", model_name)
        label_map = kwargs.get("label_map", None)

        if model_name is None:
            raise ValueError("huggingface models require 'model_name'")

        model = HuggingFaceModel(
            model_name=model_name,
            model_path=model_path,
            label_map=label_map
        )

        tokenizer = HuggingFaceTokenizer(
            tokenizer=model.pipeline.tokenizer,
            model_config=model.pipeline.model.config
        )

    elif model_type == "detoxify":
        model_name = kwargs.get("model_name", "detoxify")
        label_map = kwargs.get("label_map", None)
        threshold = kwargs.get("threshold", 0.05)

        model = DetoxifyModel(
            model_name=model_name,
            threshold=threshold
        )

        # 🔥 Important: Detoxify tokenizer reuse
        tokenizer = DetoxifyTokenizer(
            tokenizer=model.pipeline.tokenizer,
            model_config=model.pipeline.model.config
        )

    else:
        raise ValueError(f"Unknown model type: {model_type}")

    return model, tokenizer