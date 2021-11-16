FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /

RUN pip install -r /requirements.txt \
	&& rm -rf /root/.cache

COPY ./ ./

EXPOSE 8050

ENTRYPOINT ["gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "index:server"]