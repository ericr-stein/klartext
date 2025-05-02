# KlartextZH – Language Simplification App

**Production code for KlartextZH**, the **Language Simplification App of the Cantonal Administration**.

## Installation

- `pip install -r requirements.txt`
- `pip install git+https://github.com/machinelearningZH/zix_understandability-index`
- Install the required Spacy language model: `python -m spacy download de_core_news_sm`

## Setup Logging

### Configure Prometheus

- Create `prometheus.yml`

```
global:
  scrape_interval: 5s  # Scrape metrics every 5 seconds

scrape_configs:
  - job_name: 'python_app'
    static_configs:
      - targets: ['localhost:8000']
```

- Start Prometheus: `prometheus --config.file=prometheus.yml``

- Install Grafana
- Set up Grafana to use Prometheus as a data source. The default server URL of Prometheus is `http://localhost:9090`.
- Go to Grafanas Web UI at `http://localhost:3000`.
- Create a dashboard with panels for:
  - Request counts by operation/model
  - Processing times
  - Text complexity before/after
  - Input/output word counts

## Observations from Log Data of the Prototype App

The following observations were derived from the log data of the prototype app, which has been operational since **December 14, 2023**. The following analysis covers all interactions until 25th of January 2025.

- Users simplified **6,482 texts in total**, all of which were real-world inputs. Example texts were excluded from the analysis.
- In **2024**, average usage was approximately **17 texts per day, 117 per week, and 509 per month**.
- **83% of interactions were text simplifications**, while the remaining 17% were text analysises.
- Among the simplifications, **87% were performed in the "Einfache Sprache" mode**, with the remaining 13% in "Leichte Sprache."
- **15% of simplifications used the "One-Click" mode.**
- The primary model choices were **GPT-4** and **GPT-4o**. However, these were also the default settings.
- **Median response time for text simplifications was 2.6 seconds**, with an average of 4.3 seconds.  
  - **50% of responses** were delivered within **1.5 to 5 seconds**.
  - **90% of responses** were delivered within **1 to 13 seconds**.
- The app has been highly reliable, with only **0.3% failed responses**.
- Input texts had a **median word count of 36** and an average of 66.  
  - **50% of texts** ranged from 16 to 73 words.
  - **90% of texts** were between 5 and 210 words.
  - Minimum input was 1 word, and the maximum was 1,307 words.
  - 99% of texts had a length of 527 words or less.
- It’s important to note that the **text input area’s size in the current prototype app may encourage users to input shorter texts**, as these "seem to fit" better. Also currently, input is capped at **10,000 characters**.
- **64% of texts are of CEFR level C1 and C2**.
  - **The median ZIX score is -3.2**.
  - 50% of the texts have a score between -5.4 and -0.9.
  - There is a significant peak at the lower end of understandability: 7% percent of texts have a ZIX score of -9 or less.

### Conclusions

1. **Focus on excellent quality for "Einfache Sprache":** This mode represents the majority of usage and is the primary driver of interactions.
2. **Optimize for Short to Mid-Length Texts:** Given the observed input lengths, prioritizing texts between **30 to 60 words** seems sensible. Most texts won't exceed the length of a "Normseite" (~250 words). If needed, we could **limit input to ~500 words** without significantly impacting user needs.
3. **Optimize for difficult input texts**: The mayority of input texts are really hard to understand (CEFR C1 or worse).
3. **Emphasize Simplification:** Text simplification is the main use case, with text *analysis* being secondary.
4. **Prioritize Fast Response Times:** Aim to maintain **4-5 seconds on average** with a **maximum of 10-12 seconds**, as achieved in the prototype app. To improve perceived performance we also can **stream output**. This hasn't been a feature in the prototype app yet but might be a big plus from a users perspective.
