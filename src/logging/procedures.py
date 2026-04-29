from loguru import logger

def initialize_log_sinks(env: dict[str, str]) -> None:
    sink_dir: str = env["LOG_SINK_DIR"]
    sink_file: str = env["LOG_SINK_FILE"]
    logger.remove()  # Remove logging to stderr so that logs don't appear on the CLI
    logger.add(sink_dir + "/" + sink_file)