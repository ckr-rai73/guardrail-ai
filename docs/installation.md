# Installation

You can run Guardrail.ai Community Edition locally using Docker or via pip.

## Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/ckr-rai73/guardrail-ai.git
   cd guardrail-ai
   ```

2. Start the stack:
   ```bash
   docker-compose up -d
   ```

3. Access the API at `http://localhost:8000/docs`.

## Using pip

1. Ensure you have Python 3.11+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
