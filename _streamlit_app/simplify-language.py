# ---------------------------------------------------------------
# Imports

import streamlit as st

st.set_page_config(layout="wide")

import re
from datetime import datetime
import time
import base64
from docx import Document
from docx.shared import Pt, Inches
import io
import logging

import numpy as np
from zix.understandability import get_zix, get_cefr
from llama_cpp import Llama

from utils_sample_texts import SAMPLE_TEXT_01

from utils_prompts import (
    SYSTEM_MESSAGE_EASIER,
    SYSTEM_MESSAGE_ES,
    SYSTEM_MESSAGE_LS,
    RULES_EASIER,
    RULES_ES,
    RULES_LS,
    REWRITE_COMPLETE,
    OPENAI_TEMPLATE_EASIER,
    OPENAI_TEMPLATE_ES,
    OPENAI_TEMPLATE_LS,
    OPENAI_TEMPLATE_ANALYSIS_EASIER,
    OPENAI_TEMPLATE_ANALYSIS_ES,
    OPENAI_TEMPLATE_ANALYSIS_LS,
)

OPENAI_TEMPLATES = [
    OPENAI_TEMPLATE_EASIER,
    OPENAI_TEMPLATE_ES,
    OPENAI_TEMPLATE_LS,
    OPENAI_TEMPLATE_ANALYSIS_EASIER,
    OPENAI_TEMPLATE_ANALYSIS_ES,
    OPENAI_TEMPLATE_ANALYSIS_LS,
]

# ---------------------------------------------------------------
# Logging with Graphana and Prometheus

from prometheus_client import Counter, Histogram, Gauge

from streamlit_extras.prometheus import streamlit_registry
# https://arnaudmiribel.github.io/streamlit-extras/extras/prometheus/
# To produce accurate metrics, we need to ensure that unique metric objects are shared across app runs and sessions. Either 1) initialize metrics in a separate file and import them in the main app script, or 2) initialize metrics in a cached function (and ensure the cache is not cleared during execution).
# For an app running locally we can view the output with curl localhost:8501/_stcore/metrics or equivalent.


@st.cache_resource
def get_metrics():
    """Get metrics from Prometheus."""

    registry = streamlit_registry()

    # Configure standard logging for errors
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("simplify-language")

    # Define metrics with unique prefix and connect to our registry
    REQUEST_COUNT = Counter(
        "simplify_app_requests_total",
        "Total number of requests",
        ["operation", "simplification_level", "model", "success"],
        registry=registry,
    )
    PROCESSING_TIME = Histogram(
        "simplify_app_processing_seconds",
        "Time spent processing requests",
        ["operation", "simplification_level", "model"],
        buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0),
        registry=registry,
    )
    INPUT_WORD_COUNT = Histogram(
        "simplify_app_input_word_count",
        "Number of words in input text",
        buckets=(10, 50, 100, 200, 500, 1000, 2000, 5000),
        registry=registry,
    )
    OUTPUT_WORD_COUNT = Histogram(
        "simplify_app_output_word_count",
        "Number of words in output text",
        buckets=(10, 50, 100, 200, 500, 1000, 2000, 5000),
        registry=registry,
    )
    TEXT_COMPLEXITY_SCORE = Gauge(
        "simplify_app_text_complexity_score",
        "Text complexity score before and after processing",
        ["stage"],  # 'input' or 'output'
        registry=registry,
    )
    ACTIVE_USERS = Gauge(
        "simplify_app_active_users", "Number of active users", registry=registry
    )
    return (
        REQUEST_COUNT,
        PROCESSING_TIME,
        INPUT_WORD_COUNT,
        OUTPUT_WORD_COUNT,
        TEXT_COMPLEXITY_SCORE,
        ACTIVE_USERS,
        logger,
    )


(
    REQUEST_COUNT,
    PROCESSING_TIME,
    INPUT_WORD_COUNT,
    OUTPUT_WORD_COUNT,
    TEXT_COMPLEXITY_SCORE,
    ACTIVE_USERS,
    logger,
) = get_metrics()


# ---------------------------------------------------------------
# Constants


# Llama.cpp parameters.
MODEL_PATHS = {
    "Llama 3.1 3B": "_models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "Llama 3.1 Nemotron": "_models/Llama-3.2-1B-Instruct-IQ3_M.gguf",
    "Llama 3.1 «Sauerkraut»": "_models/Llama-3.2-1B-Instruct-IQ3_M.gguf",
    "Gemma 2": "_models/Llama-3.2-1B-Instruct-IQ3_M.gguf",
    "Phi-4": "_models/Llama-3.2-1B-Instruct-IQ3_M.gguf",
    "Llama 3.3": "_models/Llama-3.2-1B-Instruct-IQ3_M.gguf",
}
N_GPU_LAYERS = -1
N_CTX = 4096
N_THREADS = 16
FLASH_ATTN = True
VERBOSE = False

# From our testing we derive a sensible temperature of 0.5 as a good trade-off between creativity and coherence.
TEMPERATURE = 0.5
MAX_TOKENS = 8192

# Height of the text areas for input and output.
TEXT_AREA_HEIGHT = 600

# Maximum number of characters for the input text.
# This is way below the context window sizes of the models.
# We can increase this. However, we found that users can work and validate better when we nudge to work with shorter texts.
MAX_CHARS_INPUT = 10_000


USER_WARNING = """Mit dieser App kannst du Texte sprachlich vereinfachen. Dazu schicken wir deinen Text an ein Sprachmodell (LLM), das wir im Kanton auf einem AFI-Server betreiben. Die Server stehen im kantonseigenen Rechenzentrum (on premise). Deine Daten werden nicht gespeichert. Daher kannst du auch **vertraulich Daten verarbeiten**. Beachtet bitte, dass Sprachmodelle Fehler machen können. Die App liefert lediglich einen Entwurf. Überprüfe das Ergebnis immer und passe es an, wenn nötig. Gib uns jederzeit [Feedback](mailto:patrick.arnecke@statistik.ji.zh.ch). 🚀 Aktuelle App-Version ist v.01. Die letzte Aktualisierung war am 24.3.2025."""


# Constants for the formatting of the Word document that can be downloaded.
FONT_WORDDOC = "Arial"
FONT_SIZE_HEADING = 12
FONT_SIZE_PARAGRAPH = 9
FONT_SIZE_FOOTER = 7
DEFAULT_OUTPUT_FILENAME = "Ergebnis.docx"
ANALYSIS_FILENAME = "Analyse.docx"


# Limits for the understandability score to determine if the text is easy, medium or hard to understand.
LIMIT_HARD = -2
LIMIT_MEDIUM = 0

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------
# Functions


@st.cache_resource
def get_llamacpp_model(
    model_path,
    n_gpu_layers=N_GPU_LAYERS,
    n_ctx=N_CTX,
    n_threads=N_THREADS,
    flash_attn=FLASH_ATTN,
    verbose=VERBOSE,
):
    """Instantiate the LLM.

    Args:
        model_path (str): Path to the model.
        n_gpu_layers (int): Number of layers to offload to the GPU. -1 means all layers are offloaded to the GPU.
        n_ctx (int): Context window size.
        n_threads (int): Number of threads.
        flash_attn (bool): Experimental feature.
        verbose (bool): Set to False for production.

    Returns:
        Llama: llama.cpp model.

    """
    return Llama(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        n_ctx=n_ctx,
        n_threads=n_threads,
        flash_attn=flash_attn,
        verbose=verbose,
    )


@st.cache_resource
def get_project_info():
    """Get markdown for project information that is shown in the expander section at the top of the app."""
    with open("utils_expander.md") as f:
        return f.read()


@st.cache_resource
def create_project_info(project_info):
    """Create expander for project info. Add the image in the middle of the content."""
    with st.expander("Detaillierte Informationen zum Projekt"):
        project_info = project_info.split("### Image ###")
        st.markdown(project_info[0], unsafe_allow_html=True)
        st.image("zix_scores_validation_de.jpg", use_container_width=True)
        st.markdown(project_info[1], unsafe_allow_html=True)


def create_prompt(
    text,
    prompt_easy,
    prompt_es,
    prompt_ls,
    analysis_easy,
    analysis_es,
    analysis_ls,
    analysis,
):
    """Create prompt and system message according the app settings."""
    completeness = REWRITE_COMPLETE
    if simplification_level == "Verständlichere Sprache":
        final_prompt = prompt_easy.format(
            completeness=completeness, rules=RULES_EASIER, prompt=text
        )
        if analysis:
            final_prompt = analysis_easy.format(
                completeness=completeness, rules=RULES_EASIER, prompt=text
            )
        system = SYSTEM_MESSAGE_EASIER
    elif simplification_level == "Einfache Sprache":
        final_prompt = prompt_es.format(
            completeness=completeness, rules=RULES_ES, prompt=text
        )
        if analysis:
            final_prompt = analysis_es.format(rules=RULES_ES, prompt=text)
        system = SYSTEM_MESSAGE_ES
    else:
        final_prompt = prompt_ls.format(
            completeness=completeness, rules=RULES_LS, prompt=text
        )
        if analysis:
            final_prompt = analysis_ls.format(rules=RULES_LS, prompt=text)
        system = SYSTEM_MESSAGE_LS
    return final_prompt, system


def call_llm(
    text,
    model_id=MODEL_PATHS["Llama 3.1 Nemotron"],
    analysis=False,
):
    """Invoke LLM."""
    final_prompt, system = create_prompt(text, *OPENAI_TEMPLATES, analysis)
    try:
        message = llm.create_chat_completion(
            model=model_id,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": final_prompt},
            ],
        )
        message = message["choices"][0]["message"]["content"].strip()
        message = get_result_from_response(message)
        message = strip_markdown(message)
        return True, message
    except Exception as e:
        print(f"Error: {e}")
        return False, e


def get_result_from_response(response):
    """Extract text between tags from response."""
    if simplification_level == "Verständlichere Sprache":
        tag = "verständlichesprache"
    elif simplification_level == "Einfache Sprache":
        tag = "einfachesprache"
    else:
        tag = "leichtesprache"
    result = re.findall(rf"<{tag}>(.*?)</{tag}>", response, re.DOTALL)
    return "\n".join(result).strip()


def strip_markdown(text):
    """Strip markdown from text."""
    # Remove markdown headers.
    text = re.sub(r"#+\s", "", text)
    # Remove markdown italic and bold.
    text = re.sub(r"\*\*|\*|__|_", "", text)
    return text


def enter_sample_text():
    """Enter sample text into the text input in the left column."""
    st.session_state.key_textinput = SAMPLE_TEXT_01


def create_download_link(text_input, response, analysis=False):
    """Create a downloadable Word document and download link of the results."""
    document = Document()

    h1 = document.add_heading("Ausgangstext")
    p1 = document.add_paragraph("\n" + text_input)

    if analysis:
        h2 = document.add_heading(f"Analyse von Sprachmodell {model_choice}")
    else:
        h2 = document.add_heading("Vereinfachter Text von Sprachmodell")

    p2 = document.add_paragraph(response)
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    models_used = model_choice
    footer = document.sections[0].footer
    footer.paragraphs[
        0
    ].text = f"Erstellt am {timestamp} mit der App «KlartextZH» des Kantons Zürich.\nSprachmodell(e): {models_used}\nVerarbeitungszeit: {time_processed:.1f} Sekunden"

    # Set font for all paragraphs.
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            run.font.name = FONT_WORDDOC

    # Set font size for all headings.
    for paragraph in [h1, h2]:
        for run in paragraph.runs:
            run.font.size = Pt(FONT_SIZE_HEADING)

    # Set font size for all paragraphs.
    for paragraph in [p1, p2]:
        for run in paragraph.runs:
            run.font.size = Pt(FONT_SIZE_PARAGRAPH)

    # Set font and font size for footer.
    for run in footer.paragraphs[0].runs:
        run.font.name = "Arial"
        run.font.size = Pt(FONT_SIZE_FOOTER)

    section = document.sections[0]
    section.page_width = Inches(8.27)  # Width of A4 paper in inches
    section.page_height = Inches(11.69)  # Height of A4 paper in inches

    io_stream = io.BytesIO()
    document.save(io_stream)

    # # A download button resets the app. So we use a link instead.
    # https://github.com/streamlit/streamlit/issues/4382#issuecomment-1223924851
    # https://discuss.streamlit.io/t/creating-a-pdf-file-generator/7613?u=volodymyr_holomb

    b64 = base64.b64encode(io_stream.getvalue())
    file_name = DEFAULT_OUTPUT_FILENAME
    caption = "Vereinfachten Text herunterladen"

    if analysis:
        caption = "Analyse herunterladen"
        file_name = ANALYSIS_FILENAME
    download_url = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{file_name}">{caption}</a>'
    st.markdown(download_url, unsafe_allow_html=True)


def clean_log(text):
    """Remove linebreaks and tabs from log messages that otherwise would yield problems when parsing the logs."""
    return text.replace("\n", " ").replace("\t", " ")


def log_event(
    text,
    response,
    do_analysis,
    do_simplification,
    simplification_level,
    model_choice,
    time_processed,
    success,
):
    """Log metrics to Prometheus."""
    operation = "analysis" if do_analysis else "simplification"

    try:
        # Count the request
        REQUEST_COUNT.labels(
            operation=operation,
            simplification_level=simplification_level,
            model=model_choice,
            success=str(success),
        ).inc()

        # Record processing time
        PROCESSING_TIME.labels(
            operation=operation,
            simplification_level=simplification_level,
            model=model_choice,
        ).observe(time_processed)

        # Record text length metrics
        input_word_count = len(text.split())
        output_word_count = (
            len(response.split()) if success and isinstance(response, str) else 0
        )

        INPUT_WORD_COUNT.observe(input_word_count)
        if success and output_word_count > 0:
            OUTPUT_WORD_COUNT.observe(output_word_count)

        # Standard logging for backup/debugging
        logger.info(
            f"Operation: {operation}, Model: {model_choice}, Level: {simplification_level}, "
            f"Success: {success}, Time: {time_processed:.3f}s, "
            f"Words: {input_word_count}->{output_word_count}"
        )
    except Exception as e:
        # Ensure logging errors don't crash the application
        logger.error(f"Error logging metrics: {e}")


# ---------------------------------------------------------------
# Main

project_info = get_project_info()

if "key_textinput" not in st.session_state:
    st.session_state.key_textinput = ""

st.markdown("## 🙋‍♀️ KlartextZH - Sprache einfach vereinfachen")
create_project_info(project_info)
st.caption(USER_WARNING, unsafe_allow_html=True)
st.markdown("---")

# Set up first row with all buttons and settings.
button_cols = st.columns([1, 1, 1, 2])
with button_cols[0]:
    st.button(
        "Beispiel einfügen",
        on_click=enter_sample_text,
        use_container_width=True,
        help="Fügt einen Beispieltext ein.",
    )
with button_cols[1]:
    do_simplification = st.button(
        "Vereinfachen",
        use_container_width=True,
        help="Vereinfacht deinen Ausgangstext.",
    )
    do_analysis = st.button(
        "Analysieren",
        use_container_width=True,
        help="Analysiert deinen Ausgangstext Satz für Satz.",
    )


with button_cols[2]:
    simplification_level = st.radio(
        label="Grad der Vereinfachung",
        options=["Verständlichere Sprache", "Einfache Sprache", "Leichte Sprache"],
        index=1,
        help="**«Verständlichere Sprache»** überarbeitet den Text vorsichtiger und zielt auf Sprachniveau B2. **«Einfache Sprache»** formuliert nach den Regeln für Einfache Sprache und zielt auf B1 bis A2. **«Leichte Sprache»** folgt den Regeln für Leichte Sprache und zielt auf A2 bis A1.",
    )
    # condense_text = st.toggle(
    #     "Text verdichten",
    #     help="**Schalter aktiviert**: Modell konzentriert sich auf essentielle Informationen und versucht, Unwichtiges wegzulassen. **Schalter nicht aktiviert**: Modell versucht, alle Informationen zu übernehmen.",
    # )

with button_cols[3]:
    model_choice = st.radio(
        label="Sprachmodell",
        options=([model_name for model_name in MODEL_PATHS.keys()]),
        index=0,
        horizontal=True,
        help="Alle Modelle liefern je nach Ausgangstext meist gute bis sehr gute Ergebnisse und sind alle einen Versuch wert. Mehr Details siehe Infobox oben auf der Seite.",
    )

# Instantiate empty containers for the text areas.
cols = st.columns([2, 2, 1])

with cols[0]:
    source_text = st.container()
with cols[1]:
    placeholder_result = st.empty()
with cols[2]:
    placeholder_analysis = st.empty()


# Populate containers.
with source_text:
    st.text_area(
        "Ausgangstext, den du vereinfachen möchtest",
        value=None,
        height=TEXT_AREA_HEIGHT,
        max_chars=MAX_CHARS_INPUT,
        key="key_textinput",
    )
with placeholder_result:
    text_output = st.text_area(
        "Ergebnis",
        value=" ",
        height=TEXT_AREA_HEIGHT,
    )
with placeholder_analysis:
    text_analysis = st.metric(
        label="Verständlichkeit",
        value=None,
        delta=None,
        help="Texte in Einfacher Sprache haben meist einen Wert 0 oder höher, Texte in Leichter Sprache haben Werte von 2 oder höher.",
    )


# Derive model_id from explicit model_choice.
model_id = MODEL_PATHS[model_choice]
llm = get_llamacpp_model(model_id)

# Start processing if one of the processing buttons is clicked.
if do_simplification or do_analysis:
    start_time = time.time()
    if st.session_state.key_textinput == "":
        st.error("Bitte gib einen Text ein.")
        st.stop()

    score_source = get_zix(st.session_state.key_textinput)
    TEXT_COMPLEXITY_SCORE.labels(stage="input").set(score_source)
    # We add 0 to avoid negative zero.
    score_source_rounded = int(np.round(score_source, 0) + 0)
    cefr_source = get_cefr(score_source)

    # Analyze source text and display results.
    with source_text:
        if score_source < LIMIT_HARD:
            st.markdown(
                f"Dein Ausgangstext ist **:red[schwer verständlich]**. (Wert: {score_source_rounded}). Das entspricht grob geschätzt dem **:red[Sprachniveau {cefr_source}]**."
            )
        elif score_source >= LIMIT_HARD and score_source < LIMIT_MEDIUM:
            st.markdown(
                f"Dein Ausgangstext ist **:orange[durchschnittlich verständlich]**. (Wert: {score_source_rounded}). Das entspricht grob geschätzt dem **:orange[Sprachniveau {cefr_source}]**."
            )
        else:
            st.markdown(
                f"Dein Ausgangstext ist **:green[gut verständlich]**. (Wert: {score_source_rounded}). Das entspricht grob geschätzt dem **:green[Sprachniveau {cefr_source}]**."
            )
        with placeholder_analysis.container():
            text_analysis = st.metric(
                label="Verständlichkeit",
                value=score_source_rounded,
                delta=None,
                help="Verständlichkeit auf einer Skala von -10 bis 10 Punkten (von -10 = extrem schwer verständlich bis 10 = sehr gut verständlich). Texte in Einfacher Sprache haben meist einen Wert von 0 bis 4 oder höher, Texte in Leichter Sprache 2 bis 6 oder höher.",
            )

        with placeholder_analysis.container():
            with st.spinner("Ich arbeite..."):
                success, response = call_llm(
                    st.session_state.key_textinput,
                    model_id=model_id,
                    analysis=do_analysis,
                )

    if success is False:
        st.error(
            "Es ist ein Fehler bei der Abfrage aufgetreten. Bitte versuche es erneut."
        )
        time_processed = time.time() - start_time
        log_event(
            st.session_state.key_textinput,
            "Error from modell call.",
            do_analysis,
            do_simplification,
            simplification_level,
            model_choice,
            time_processed,
            success,
        )

        st.stop()

    # Display results in UI.
    text = "Dein vereinfachter Text"
    if do_analysis:
        text = "Deine Analyse"
    # Often the models return the German letter ß as ss. Replace it.
    response = response.replace("ß", "ss")
    time_processed = time.time() - start_time
    with placeholder_result.container():
        st.text_area(
            text,
            height=TEXT_AREA_HEIGHT,
            value=response,
        )
        if do_simplification:
            score_target = get_zix(response)
            TEXT_COMPLEXITY_SCORE.labels(stage="output").set(score_target)
            score_target_rounded = int(np.round(score_target, 0) + 0)
            cefr_target = get_cefr(score_target)
            if score_target < LIMIT_HARD:
                st.markdown(
                    f"Dein vereinfachter Text ist **:red[schwer verständlich]**. (Wert: {score_target_rounded}). Das entspricht etwa dem **:red[Sprachniveau {cefr_target}]**."
                )
            elif score_target >= LIMIT_HARD and score_target < LIMIT_MEDIUM:
                st.markdown(
                    f"Dein Ausgangstext ist **:orange[durchschnittlich verständlich]**. (Wert: {score_target_rounded}). Das entspricht grob geschätzt dem **:orange[Sprachniveau {cefr_target}]**."
                )
            else:
                st.markdown(
                    f"Dein vereinfachter Text ist **:green[gut verständlich]**. (Wert: {score_target_rounded}). Das entspricht etwa dem **:green[Sprachniveau {cefr_target}]**."
                )
            with placeholder_analysis.container():
                text_analysis = st.metric(
                    label="Verständlichkeit",
                    value=score_target_rounded,
                    delta=int(np.round(score_target - score_source, 0)),
                    help="Verständlichkeit auf einer Skala von -10 bis 10 (von -10 = extrem schwer verständlich bis 10 = sehr gut verständlich). Texte in Einfacher Sprache haben meist einen Wert von 0 bis 4 oder höher.",
                )

                create_download_link(st.session_state.key_textinput, response)
                st.caption(f"Verarbeitet in {time_processed:.1f} Sekunden.")
        else:
            with placeholder_analysis.container():
                text_analysis = st.metric(
                    label="Verständlichkeit 0-20",
                    value=score_source_rounded,
                    help="Verständlichkeit auf einer Skala von -10 bis 10 (von -10 = extrem schwer verständlich bis 10 = sehr gut verständlich). Texte in Einfacher Sprache haben meist einen Wert von 0 bis 4 oder höher.",
                )
                create_download_link(
                    st.session_state.key_textinput, response, analysis=True
                )
                st.caption(f"Verarbeitet in {time_processed:.1f} Sekunden.")

        log_event(
            st.session_state.key_textinput,
            response,
            do_analysis,
            do_simplification,
            simplification_level,
            model_choice,
            time_processed,
            success,
        )
        st.stop()
