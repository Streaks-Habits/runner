FROM alpine as main

# Install daemons dependencies
RUN apk add --no-cache python3 py3-pip tzdata
# Copy sources and builded sources
WORKDIR /cli
COPY src src
COPY requirements.txt .
# Install dependencies
RUN pip3 install -r requirements.txt

CMD sh -c "python src/runner.py"
