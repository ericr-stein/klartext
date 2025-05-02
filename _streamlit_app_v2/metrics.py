import os
from prometheus_client import Counter, Histogram, Summary, start_http_server, REGISTRY
import threading


def get_metric(metric_cls, name, *args, **kwargs):
    try:
        # Try to find the metric in the registry
        return REGISTRY._names_to_collectors[name]
    except KeyError:
        # Not found, create a new one
        return metric_cls(name, *args, **kwargs)


REQUEST_COUNT = get_metric(
    Counter,
    "simplify_requests_total",
    "Total number of simplification requests",
    ["simplification_level", "model", "success"],
)

PROCESSING_TIME = get_metric(
    Histogram,
    "simplify_processing_seconds",
    "Time spent processing requests",
    ["simplification_level", "success"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
)

INPUT_WORD_COUNT = get_metric(
    Summary, "simplify_input_words", "Number of words in input text"
)

OUTPUT_WORD_COUNT = get_metric(
    Summary, "simplify_output_words", "Number of words in output text"
)

ZIX_INPUT_TEXT = get_metric(Summary, "zix_input_text", "Zix input text")
ZIX_OUTPUT_TEXT = get_metric(Summary, "zix_output_text", "Zix output text")


def track_metrics(
    input_words,
    output_words,
    zix_input_text,
    zix_output_text,
    simplification_level,
    model_choice,
    time_processed,
    success,
):
    REQUEST_COUNT.labels(
        simplification_level=simplification_level,
        model=model_choice,
        success=str(success),
    ).inc()
    PROCESSING_TIME.labels(
        simplification_level=simplification_level, success=str(success)
    ).observe(time_processed)

    INPUT_WORD_COUNT.observe(input_words)

    if success:
        OUTPUT_WORD_COUNT.observe(output_words)

    ZIX_INPUT_TEXT.observe(zix_input_text)
    ZIX_OUTPUT_TEXT.observe(zix_output_text)


def start_metrics_server(port=8000, addr="0.0.0.0"):
    try:
        start_http_server(port, addr)
        print(f"Prometheus metrics server started on {addr}:{port}")
    except Exception as e:
        print(f"Failed to start metrics server: {e}")


metrics_port = int(os.environ.get("METRICS_PORT", "8000"))
threading.Thread(target=start_metrics_server, args=(metrics_port,), daemon=True).start()
