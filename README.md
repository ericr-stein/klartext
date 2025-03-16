# Language Simplification App KTZH

Production code and quality evaluations for the **Language Simplification App of the Cantonal Administration**.

## Installation

- `pip install -r requirements.txt`
- `pip install git+https://github.com/machinelearningZH/zix_understandability-index`
- Install the required Spacy language model: `python -m spacy download de_core_news_sm`

## Setup Logging

- Configure Prometheus to scrape the metrics endpoint at port 8000
- Set up Grafana to use Prometheus as a data source
- Create a dashboard with panels for:
  - Request counts by operation/model
  - Processing times
  - Text complexity before/after
  - Input/output word counts

  Prometheus configuration example:

  ```
  scrape_configs:
  - job_name: 'simplify-language'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
  ```

## Observations from Log Data

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

## Evaluate OSS LLMs

We need to select an **Open Weights LLM** suitable for our text simplification service. Below are the evaluation criteria and the current shortlist.

### Base Requirements

1. **Commercially Viable License:** Must have a license like MIT, Apache, etc.
2. **German Language Support:** The model should work effectively with German texts.
3. **Resource Compatibility:** Must fit within available server RAM/VRAM.
4. **Performance:** Should meet performance expectations (tokens per second) for our use case.

**Note:** Context size is not critical as most user texts are short and input can be limited. Prompts average **1.5k tokens**.

### Evaluation Criteria

1. **General vibe**.
2. **Human Expert Feedback:** E.g. assessments by experts from ZHweb-Team or Comm-Team StVA.
3. **Prompt Compatibility:** Should work with existing prompts, though adaptations are acceptable.
4. **Simplification Modes:** Should produce good results in the three simplification modes:
   - "Einfache Sprache" (our main focus)
   - "Verständlichere Sprache"
   - "Leichte Sprache"
5. **Reliability:** Consistent outputs, such as:
   - Proper XML tags (important since JSON often fails with embedded quotes).
   - Adherence to German (no foreign language interspersed) and German language standards, including grammar and syntax.
6. **Improved Understandability:** Demonstrable improvement in understandability measured using our **ZIX score**.
7. **Accuracy:** Minimal factual errors or hallucinations. Evaluated using LLM judgment aligned with human preferences.

**Note:** Completeness is less critical. We recognize that some factual simplification is inherent to language simplification and may trade off with completeness. We may add a feature that tells the user, what parts of the content were omitted in the simplified text version (this is an actual backlog item for our prototype app).

### Current Shortlist

The candidates under consideration are these:

- [Phi4 14B (Q6_K_L)](https://huggingface.co/bartowski/phi-4-GGUF)
- [Phi4 14B Unsloth (Q5_K_M)](https://huggingface.co/unsloth/phi-4-GGUF)
- [Llama 3.1 SauerkrautLM 70B (Q5_K_M)](https://huggingface.co/mradermacher/Llama-3.1-SauerkrautLM-70b-Instruct-GGUF)
- [Llama 3.1 Nemotron 70B (Q5_K_M)](https://huggingface.co/bartowski/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF)
- [Llama 3.2 3B](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF)
- [Llama 3.3 70B (Q5_K_M)](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF)
- [Gemma 2 27B (Q5_K_M)](https://huggingface.co/bartowski/gemma-2-27b-it-GGUF)
- [Gemma 3 27B (Q5_K_M and Q6_k)](https://huggingface.co/unsloth/gemma-3-27b-it-GGUF)
- [Qwen 2.5 32B (Q5_K-M)](https://huggingface.co/bartowski/Qwen2.5-32B-Instruct-GGUF)
- [Qwen 2.5 72B (Q5_K-M)](https://huggingface.co/bartowski/EVA-Qwen2.5-72B-v0.2-GGUF)
- [Mistral Small v3 24B](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501)

Reasoning models

- [QwQ 32B (Q5_K-M)](https://huggingface.co/unsloth/QwQ-32B-GGUF)
- [Deepseek R1 Distill Llama 8B (Q5_K-M)](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF)
- [Deepseek R1 Distill Llama 70B (Q4_K-M)](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF)

**Quantization Considerations:** The **degree of quantization** has to be discussed too. **Q4 and Q5** appears to offer an optimal balance between performance and resource efficiency.

### Finetuning

While we may explore **finetuning** in the future, our current focus is on **identifying a strong base model** and establishing a **robust evaluation pipeline**. Finetuning will be pursued if necessary.

### Creating a Test Set

- We selected 40 representative input texts from actual user inputs.
- We added 10 additional texts mainly from our website.
- The samples have a length between 27 and 259 words (median 111).
- The samples have a ZIX score between -10 and -0.2.
- The CEFR levels are C2 (25), C1 (18) and B2 (7).

### Results

**The best models overall are:**

- **Llama 3.1 Nemotron 70B (Q5_K_M)**
- **Llama 3.1 SauerkrautLM 70B (Q5_K_M)**
- **Gemma 2 27B (Q5_K_M)**
- **Gemma 3 27B (Q6_k)**
- **Phi-4 Unsloth 14B (Q5_K_M)**

**Llama 3.3 70B (Q5_K_M) yields the best results for Leichte Sprache.**

All other models yield less good results. We do not recommend these for our use case.

Proprietary models like GPT-4o and Claude Sonnet v3.5 outperfom all open source models in the vibe check. They are also very good in terms of understandability and in the top group of models considering the wide confidence interval of our correctness measurements. The good news here is, that our best OSS models are not far behind.
