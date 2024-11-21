# JASS
### Overview
Our main goal is to create a tool for researchers which will make the process easier and simplify the way for getting up-to-date information.

###  Problem Statement (technology perspective)
It takes long time to find relevant and up-to-date information daily. Good to have brief overview of new tecnologies.

### Objectives
- Objective 1: Simplify the process of recieving up-to-date information on daily basis
- Objective 2: Asistance for the researcher on filtering the information
- Objective 3: Guidance for the person to advice next steps

### Features
- Feature 1: Summary of all papers that were released today.
- Feature 2: Search of the code bases that suit the papers for the selected topics of research (to give code examples).
- Feature 3: Filtering of the main papers by topic or by tecnical parametrs (limitations)
- Feature 4: Customers feedback that can affect the answer to give more relevant results
- Feature 5: Predict next steps of research, suggestions for the new topics and spheres that will help to solve current problem

### Timeline
- 18.11: Deliverables:
	- Parsing of the papers from huggingface (daily updates)
 	- Getting summary of these papers
  	- Search of code bases for the reserches found on previous steps
- 19.11: Deliverables:
	- Adding search conditions: filter by the topic
	- Adding search conditions: filter by tecnical limitations
- 20.11: Deliverables:
	- Communication with the found paper/article
 	- Customers feedback that can affect the answer to give more relevant results
- 21.11: Deliverables:
	- Reseearch forecast: predict next steps, interesting domains
### Team
- Evgenii
- Dmitry
- Alexei
- Ekaterina

### Risks and Mitigation Strategies

At least two!

| Risk   | Impact          | Probability     | Mitigation Strategy  |
| ------ | --------------- | --------------- | -------------------- |
| Risk 1 | High/Medium/Low | High/Medium/Low | Strategy description |
| Risk 2 | High/Medium/Low | High/Medium/Low | Strategy description |
### Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

### Appendix
Any additional information, references, or documents relevant to the project.


# Setting Up Python Environment with `pip` and Running Code

## 1. Creating a Virtual Environment

1. Navigate to the project directory:
   ```bash
   cd /path/to/your/project
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv jass_researcher
   ```

3. Activate the virtual environment:
   ```bash
   source jass_researcher/bin/activate
   ```

## 2. Installing Dependencies

Install dependencies:
```bash
pip install <package_name>
```

## 3. Freezing Dependencies

Create `requirements.txt`:
```bash
pip freeze > requirements.txt
```

## 4. Installing Dependencies from `requirements.txt`

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 5. Running Python Code

Activate the virtual environment:
```bash
source jass_researcher/bin/activate
```

Run a Python script:
```bash
python main.py
```
# Result of research by query 'Speakers diarization'

### ArXiv Papers
1. **[3D-Speaker-Toolkit: An Open-Source Toolkit for Multimodal Speaker Diarization](https://arxiv.org/html/2403.19971v2)**  
   Summary: The 3D-Speaker-Toolkit is an open-source toolkit designed for multimodal speaker verification and diarization, integrating acoustic, semantic, and visual data to enhance speaker recognition capabilities. It features three main modules: an acoustic module for extracting speaker embeddings using both supervised and self-supervised learning, a semantic module that utilizes advanced language models to analyze spoken language, and a visual module for facial feature analysis to improve diarization accuracy in multi-speaker settings. The toolkit includes state-of-the-art models, a large dataset of over 10,000 speakers, and is designed for easy deployment and use in research and industry. It aims to provide a robust platform for developing and deploying advanced speaker-related models, achieving superior performance in various tasks compared to traditional acoustic-only approaches. The toolkit is publicly available on GitHub.  
   Useful GitHub link: [3D-Speaker](https://github.com/modelscope/3D-Speaker)

2. **[ESPnet-SPK: full pipeline speaker embedding toolkit with state-of-the-art performance](https://arxiv.org/html/2401.17230v2)**  
   Summary: The paper presents ESPnet-SPK, an open-source toolkit for training and utilizing speaker embedding extractors. It features a modular architecture that allows easy development of various models, including x-vector and SKA-TDNN, and supports self-supervised learning (SSL) integration. The toolkit provides over 30 reproducible recipes for tasks such as speaker verification, text-to-speech, and target speaker extraction, with pre-trained models available for immediate use. Notably, it achieved a state-of-the-art equal error rate (EER) of 0.39% on the Vox1-O benchmark using WavLM-ECAPA. ESPnet-SPK aims to facilitate research in speaker recognition by offering a comprehensive platform for model development and evaluation, making advanced speaker embeddings accessible to the broader community.  
   Useful GitHub links: [s3prl](https://github.com/s3prl/s3prl), [ESPnet](https://github.com/espnet/espnet)

3. **[Disentangling Voice and Content with Self-Supervision for Speaker Diarization](https://proceedings.neurips.cc/paper_files/paper/2023/file/9d276b0a087efdd2404f3295b26c24c1-Paper-Conference.pdf)**  
   Summary: The paper introduces a novel framework named Recurrent Xi-vector (RecXi) aimed at improving speaker recognition by effectively separating speaker traits from speech content. Traditional methods struggle with this separation due to the intertwined nature of speaker characteristics and content in speech signals. The proposed framework utilizes three Gaussian inference layers to model static (speaker traits) and dynamic (content variability) components of speech. A self-supervised learning approach is employed to facilitate content disentanglement without requiring additional labeled data, relying solely on speaker identities. Experimental results on the VoxCeleb and SITW datasets demonstrate significant performance improvements, with reductions of 9.56% in equal error rate (EER) and 8.24% in minimum detection cost function (minDCF). The framework's design allows for practical application without the need for extensive retraining or additional data, making it a promising solution for real-world speaker recognition tasks. The paper concludes with future work directions, including potential applications in automatic speech recognition and voice conversion.  
   Useful GitHub link: None provided.

### Github Links
1. **[Awesome Speaker Diarization](https://github.com/wq2012/awesome-diarization)**  
   Summary: This repository is a curated collection of resources related to speaker diarization, including research papers, libraries, and tools. It serves as a comprehensive guide for researchers and practitioners in the field, providing links to state-of-the-art methods, datasets, and software implementations. The repository is regularly updated to include the latest advancements and resources in speaker diarization, making it a valuable reference for anyone interested in the topic.

2. **[3D-Speaker-Toolkit](https://github.com/3D-Speaker-Toolkit)**  
   Summary: The 3D-Speaker toolkit provides access to pretrained models via ModelScope and includes a large-scale speech corpus to support research in speech representation. It allows users to install the software, run various experiments, and perform inference using pretrained models. The toolkit features supervised and self-supervised speaker verification methods, speaker diarization, and language identification, with detailed instructions for each. Recent updates include new models and enhancements for improved performance. The toolkit is licensed under the Apache License 2.0.

3. **[ESPnet-SPK](https://github.com/espnet/espnet)**  
   Summary: ESPnet is an end-to-end speech processing toolkit that facilitates various speech-related tasks, including automatic speech recognition (ASR), text-to-speech (TTS), speech translation, speech enhancement, speaker diarization, and spoken language understanding. Built on PyTorch, it incorporates Kaldi-style data processing and feature extraction, making it suitable for diverse speech processing experiments. The toolkit is open-source, with extensive documentation, tutorials, and pre-trained models available for various tasks.

### Hugging Face Models
1. **[pyannote_SD1](https://huggingface.co/AMITKESARI2000/pyannote_SD1)**  
   Summary: This model is designed for speaker diarization, which involves identifying when different speakers are talking in an audio file. It relies on the pyannote.audio library (version 2.0) and provides a simple interface for use, demonstrated through a code snippet. The model was trained using the AMI legacy dataset, achieving a diarization error rate of 21.4% on the AMI only_words evaluation set. It has seen limited downloads (2 in the last month), and there are currently issues with determining its library compatibility for the Inference API. The model is available under the MIT license.

2. **[vad-crdnn-libriparty](https://huggingface.co/speechbrain/vad-crdnn-libriparty)**  
   Summary: This model enables the detection of speech segments in audio recordings, outputting timestamps for speech and non-speech segments. It requires audio input sampled at 16kHz and can process both short and long recordings. The model achieves high precision (0.9518) and recall (0.9437) on the LibriParty test set. The README provides installation instructions, usage examples, and details on the VAD pipeline, which includes computing posterior probabilities, applying thresholds, and optional post-processing steps to refine segment detection.

3. **[pyannote-speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)**  
   Summary: This open-source speaker diarization model is part of the pyannote.audio library. Users must agree to specific conditions to access the model's files and content, aimed at understanding the user base and supporting further development. Key features include installation instructions and usage examples for the speaker diarization pipeline, options to specify the number of speakers during processing, performance benchmarks, and a call for contributions from companies and researchers to support the model's development.

### Hugging Face Datasets
1. **[simsamu](https://huggingface.co/datasets/diarizers-community/simsamu)**  
   Summary: This dataset consists of 61 audio recordings of simulated medical dispatch dialogues in French, totaling approximately 3 hours and 15 minutes of audio. Each recording averages about 3 minutes and 11 seconds. The dataset is particularly valuable for tasks related to speaker diarization, speaker segmentation, and voice activity detection, as it includes annotations for timestamps and speaker identities. The dataset captures different communication styles, reflecting realistic dispatch situations and is available under the MIT license.

2. **[voxconverse](https://huggingface.co/datasets/diarizers-community/voxconverse)**  
   Summary: This audio-visual diarization dataset features multispeaker clips of human speech sourced from YouTube videos. It is designed for speaker diarization and voice activity detection, with files available in Parquet format. The dataset includes three splits: training, validation, and testing, totaling 448 rows. It has been preprocessed to be compatible with diarization tools and can be used to fine-tune segmentation models. The dataset is licensed under CC BY 4.0.

3. **[AMI](https://huggingface.co/datasets/diarizers-community/ami)**  
   Summary: The AMI Meeting Corpus dataset consists of 100 hours of meeting recordings in English, utilizing various audio signals and video sources. It features recordings from meetings with mostly non-native speakers across three rooms with differing acoustic properties. The dataset is preprocessed for compatibility with the diarizers library, particularly for fine-tuning pyannote segmentation models. It has seen 440 downloads in the last month and is part of a broader collection of speaker diarization datasets.

This summary provides a comprehensive overview of the latest research, models, and datasets related to speaker diarization, including SOTA models and quality metrics.




