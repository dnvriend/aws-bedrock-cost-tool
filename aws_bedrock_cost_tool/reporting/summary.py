"""Quick summary output formatting.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from aws_bedrock_cost_tool.core.models import CostData


def format_summary(cost_data: CostData) -> str:
    """Format cost data as quick summary string.

    Shows total cost and top 3 models.
    Format: "Total: $X.XX | Top: Model1 ($Y), Model2 ($Z), Model3 ($W)"

    Args:
        cost_data: Analyzed cost data

    Returns:
        Summary string
    """
    # Format total cost with estimated indicator
    if cost_data["has_estimated"]:
        total_str = f"~${cost_data['total_cost']:.2f}"
    else:
        total_str = f"${cost_data['total_cost']:.2f}"

    # Get top 3 models
    top_models = cost_data["models"][:3]

    if not top_models:
        return f"Total: {total_str} | No Bedrock usage found"

    # Format top models
    model_strs = []
    for model in top_models:
        # Shorten model name (remove " (Amazon Bedrock Edition)")
        short_name = model["model_name"].replace(" (Amazon Bedrock Edition)", "")

        # Add estimated indicator if needed
        if model["estimated"]:
            cost_str = f"~${model['total_cost']:.2f}"
        else:
            cost_str = f"${model['total_cost']:.2f}"

        model_strs.append(f"{short_name} ({cost_str})")

    top_str = ", ".join(model_strs)

    return f"Total: {total_str} | Top: {top_str}"
