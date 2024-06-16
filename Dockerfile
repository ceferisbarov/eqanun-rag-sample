FROM pytorch/pytorch

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

ADD chatbot.py /app/chatbot.py

ADD engine.py /app/engine.py

ADD sentence_tokenizer_aze /app/sentence_tokenizer_aze

ADD allmalab.png /app/allmalab.png

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
