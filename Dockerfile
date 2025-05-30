FROM dustynv/nano_llm:r36.4.0

# Create necessary directories
RUN mkdir -p /data/models/mlc/dist/models

# Copy prebuilt Hugging Face and MLC artifacts (comment out if you dont have them)
# COPY hf_models /data/models/huggingface
# COPY mlc_artifacts /data/models/mlc/dist/VILA1.5-3b

# Create symlink for the MLC model if required by NanoLLM
RUN ln -s /data/models/mlc/dist/VILA1.5-3b /data/models/mlc/dist/models/VILA1.5-3b

# Default entrypoint to launch Studio with the preset
ENTRYPOINT ["python3", "-m", "nano_llm.studio"]
CMD ["--load", "PersonDetector.json"]

