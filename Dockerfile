FROM dustynv/nano_llm:r36.4.0

# Create necessary directories
RUN mkdir -p /data/models/mlc/dist/models

# Copy model symlink fix
RUN ln -s /data/models/huggingface/models--Efficient-Large-Model--VILA1.5-3b/snapshots/42d1dda6807cc521ef27674ca2ae157539d17026/llm \
          /data/models/mlc/dist/models/VILA1.5-3b

# Set default entrypoint to NanoLLM Studio
ENTRYPOINT ["python3", "-m", "nano_llm.studio"]

# Default preset to load
CMD ["--load", "/opt/NanoLLM/nano_llm/agents/presets/PersonDetector.json"]

