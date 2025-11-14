"""CLI entry point for aws-bedrock-cost-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from aws_bedrock_cost_tool.core.analyzer import DetailLevel, analyze_cost_data
from aws_bedrock_cost_tool.core.cost_explorer import (
    CredentialsError,
    PermissionError,
    create_cost_explorer_client,
    query_bedrock_costs,
)
from aws_bedrock_cost_tool.reporting.json_formatter import format_as_json
from aws_bedrock_cost_tool.reporting.plots import plot_model_bar_chart, plot_time_series
from aws_bedrock_cost_tool.reporting.summary import format_summary
from aws_bedrock_cost_tool.reporting.table_renderer import render_table
from aws_bedrock_cost_tool.utils import (
    PeriodParseError,
    PeriodValidationError,
    calculate_date_range,
    format_date_for_aws,
    parse_period,
    validate_period,
)


@click.command()
@click.version_option(version="0.1.0")
@click.option(
    "--period",
    default="30d",
    help="Period to analyze (e.g., 7d, 2w, 1m, 3m). Max: 365d. Default: 30d.",
)
@click.option(
    "--profile",
    help="AWS profile name (overrides AWS_PROFILE environment variable)",
)
@click.option(
    "--detail",
    type=click.Choice(["basic", "standard", "full"]),
    default="standard",
    help=(
        "Detail level: basic (models only), standard (+ usage types), "
        "full (+ regions). Default: standard."
    ),
)
@click.option(
    "--table",
    is_flag=True,
    help="Show summary table instead of JSON output",
)
@click.option(
    "--plot-time",
    is_flag=True,
    help="Show time series plot of daily costs instead of JSON output",
)
@click.option(
    "--plot-models",
    is_flag=True,
    help="Show bar chart of model costs instead of JSON output",
)
@click.option(
    "--all-visual",
    is_flag=True,
    help="Show all visualizations (table + time series + bar chart) instead of JSON output",
)
@click.option(
    "--summary-only",
    is_flag=True,
    help="Show quick summary (total + top 3 models) instead of JSON output",
)
@click.option(
    "--verbose",
    "-V",
    is_flag=True,
    help="Log API calls and processing steps to stderr",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress informational messages",
)
def main(
    period: str,
    profile: str | None,
    detail: DetailLevel,
    table: bool,
    plot_time: bool,
    plot_models: bool,
    all_visual: bool,
    summary_only: bool,
    verbose: bool,
    quiet: bool,
) -> None:
    """AWS Bedrock Cost Analysis Tool

    Analyzes AWS Bedrock model costs using Cost Explorer API.
    Supports multiple output formats: JSON (default), tables, plots, and summaries.

    Examples:

    \b
    # Default: JSON output for last 30 days
    aws-bedrock-cost-tool

    \b
    # Quick summary (total + top 3 models)
    aws-bedrock-cost-tool --summary-only

    \b
    # Visual table for last 90 days
    aws-bedrock-cost-tool --period 90d --table

    \b
    # Full report with all visualizations
    aws-bedrock-cost-tool --all-visual --detail full

    \b
    # Last 2 weeks with specific profile
    aws-bedrock-cost-tool --period 2w --profile production

    \b
    # Time series plot with verbose logging
    aws-bedrock-cost-tool --plot-time --verbose

    \b
    # Pipe JSON to jq for automation
    aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
    """
    try:
        # Parse and validate period
        days = parse_period(period)
        validate_period(days)

        # Calculate date range
        start_date, end_date = calculate_date_range(days)
        start_str = format_date_for_aws(start_date)
        end_str = format_date_for_aws(end_date)

        # Create Cost Explorer client
        client = create_cost_explorer_client(profile)

        # Query costs
        response = query_bedrock_costs(client, start_str, end_str, verbose=verbose)

        # Analyze data
        cost_data = analyze_cost_data(response, start_str, end_str, detail=detail)

        # Check for empty results
        if cost_data["total_cost"] == 0:
            if not quiet:
                print(
                    f"No Bedrock costs found for period {period} ({start_str} to {end_str}).",
                    file=sys.stderr,
                )
                print(
                    "Check if Bedrock was used during this period or try a longer period.",
                    file=sys.stderr,
                )
            sys.exit(0)

        # Determine output mode
        visual_mode = table or plot_time or plot_models or all_visual or summary_only

        if visual_mode:
            # Visual output modes (to stderr)
            if summary_only:
                print(format_summary(cost_data))
            else:
                if table or all_visual:
                    render_table(cost_data, detail=detail)

                if plot_time or all_visual:
                    plot_time_series(cost_data)

                if plot_models or all_visual:
                    plot_model_bar_chart(cost_data)
        else:
            # Default: JSON to stdout
            print(format_as_json(cost_data))

    except PeriodParseError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except PeriodValidationError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    except CredentialsError as e:
        click.echo(f"AWS Credentials Error:\n{e}", err=True)
        sys.exit(1)

    except PermissionError as e:
        click.echo(f"AWS Permission Error:\n{e}", err=True)
        sys.exit(1)

    except Exception as e:
        if verbose:
            import traceback

            traceback.print_exc(file=sys.stderr)
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
