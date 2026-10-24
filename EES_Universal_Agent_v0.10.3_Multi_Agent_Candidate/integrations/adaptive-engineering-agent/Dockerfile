FROM python:3.12-slim
RUN useradd --create-home --uid 10001 agent
WORKDIR /app
COPY . /app
RUN mkdir -p /workspace /app/data && chown -R agent:agent /app /workspace
USER agent
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 AGENT_WORKSPACE=/workspace
ENTRYPOINT ["python", "/app/scripts/agent_runtime.py"]
