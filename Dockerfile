FROM dustynv/nano_llm:r36.4.0

# Create necessary directories
RUN mkdir -p /data/models/mlc/dist/models

# Copy prebuilt Hugging Face and MLC artifacts (comment out if you dont have them)
# COPY hf_models /data/models/huggingface
# COPY mlc_artifacts /data/models/mlc/dist/VILA1.5-3b

# Create symlink for the MLC model if required by NanoLLM
RUN mkdir -p /data/models/mlc/dist/models && \
    if [ ! -L /data/models/mlc/dist/models/VILA1.5-3b ]; then \
        ln -s /data/models/huggingface/models--Efficient-Large-Model--VILA1.5-3b/snapshots/42d1dda6807cc521ef27674ca2ae157539d17026/llm \
              /data/models/mlc/dist/models/VILA1.5-3b; \
    fi


# Default entrypoint to launch Studio with the preset
ENTRYPOINT ["python3", "-m", "nano_llm.studio"]
CMD ["--load", "PersonDetector.json"]

