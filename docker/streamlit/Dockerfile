FROM python:3
RUN pip install --upgrade pip
WORKDIR /usr/src/app
COPY ./docker/streamlit/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8501
COPY ../.. .
RUN chmod +x run_streamlit.sh
ENTRYPOINT ["./run_streamlit.sh"]