FROM python:3.9

ENV DST /app
ENV REQUIREMENTS requirements.txt

COPY src/bpgen ${DST}/bpgen
COPY ${REQUIREMENTS} ${DST}

WORKDIR ${DST}
RUN pip install -r ${DST}/${REQUIREMENTS}

ENV PYTHONPATH ${DST}
CMD ["python", "bpgen/main.py"]
