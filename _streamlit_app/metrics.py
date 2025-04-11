import os
import time
from prometheus_client import Counter, Histogram, Summary, Gauge, start_http_server
import threading
import logging

# Initialize Prometheus metrics
REQUEST_COUNT = Counter(
    'simplify_requests_total',
    'Total number of simplification requests',
    ['simplification_level', 'mode', 'model', 'success']
)

PROCESSING_TIME = Histogram(
    'simplify_processing_seconds',
    'Time spent processing requests',
    ['simplification_level', 'success'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

INPUT_WORD_COUNT = Summary('simplify_input_words', 'Number of words in input text')
OUTPUT_WORD_COUNT = Summary('simplify_output_words', 'Number of words in output text')
COMPRESSION_RATIO = Gauge('simplify_compression_ratio', 'Ratio of output words to input words')

def track_metrics(
    input_text,
    output_text,
    do_analysis,
    do_simplification,
    simplification_level,
    model_choice,
    time_processed,
    success
):
    """
    Track metrics for a request.

    Args:
        input_text (str): The input text
        output_text (str): The output text
        do_analysis (bool): Whether analysis was performed
        do_simplification (bool): Whether simplification was performed
        simplification_level (str): The level of simplification
        model_choice (str): The model used
        time_processed (float): Processing time in seconds
        success (bool): Whether the request was successful
    """
    # Get word counts
    input_words = len(input_text.split())
    output_words = len(output_text.split()) if success else 0

    # Use appropriate request mode
    mode = "analysis" if do_analysis else "simplification"

    # Record metrics
    REQUEST_COUNT.labels(
        simplification_level=simplification_level,
        mode=mode,
        model=model_choice,
        success=str(success)
    ).inc()

    PROCESSING_TIME.labels(
        simplification_level=simplification_level,
        success=str(success)
    ).observe(time_processed)

    INPUT_WORD_COUNT.observe(input_words)

    if success:
        OUTPUT_WORD_COUNT.observe(output_words)
        if input_words > 0:
            COMPRESSION_RATIO.set(output_words / input_words)

def start_metrics_server(port=8000, addr='0.0.0.0'):
    """
    Start the Prometheus metrics server with enhanced logging.

    Args:
        port (int): The port to listen on
        addr (str): The address to bind to (0.0.0.0 for all interfaces)
    """
    try:
        # Configure basic logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Start the HTTP server for Prometheus metrics
        start_http_server(port, addr)

        # Log success messages
        logging.warning(f"Prometheus metrics server started successfully on {addr}:{port}")
        print(f"Prometheus metrics server started on {addr}:{port}") # Keep print for immediate console feedback if needed
    except Exception as e:
        logging.error(f"Failed to start metrics server on {addr}:{port}: {e}", exc_info=True)
        print(f"FAILED to start metrics server: {e}") # Also print error

# Start the metrics server when imported with robust error handling
metrics_port_str = os.environ.get('METRICS_PORT', '8000')

# Configure basic logging if not already configured
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    # Convert port to integer
    metrics_port = int(metrics_port_str)
    logging.info(f"Starting metrics server on port {metrics_port}")

    # Ensure the thread starts reliably
    metrics_thread = threading.Thread(target=start_metrics_server, args=(metrics_port,), daemon=True)
    metrics_thread.start()
    logging.warning(f"Metrics server thread started on port {metrics_port}")

    # Give the thread a moment to start and catch any immediate errors
    time.sleep(1)

    if metrics_thread.is_alive():
        logging.info(f"Metrics server thread is running on port {metrics_port}")
    else:
        logging.error(f"Metrics server thread failed to start on port {metrics_port}")

except ValueError:
    logging.error(f"Invalid METRICS_PORT value: {metrics_port_str}. Cannot start metrics server.")
except Exception as e:
    logging.error(f"Error starting metrics server thread: {e}", exc_info=True)
