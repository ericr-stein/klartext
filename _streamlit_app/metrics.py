import os
from prometheus_client import Counter, Histogram, Summary, Gauge, start_http_server
import threading

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
    Start the Prometheus metrics server.
    
    Args:
        port (int): The port to listen on
        addr (str): The address to bind to (0.0.0.0 for all interfaces)
    """
    try:
        start_http_server(port, addr)
        print(f"Prometheus metrics server started on {addr}:{port}")
    except Exception as e:
        print(f"Failed to start metrics server: {e}")

# Start the metrics server when imported
metrics_port = int(os.environ.get('METRICS_PORT', '8000'))
threading.Thread(target=start_metrics_server, args=(metrics_port,), daemon=True).start()
