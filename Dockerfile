FROM alpine as main

# Install dependencies
RUN apk add --no-cache python3 py3-pip tzdata
# Install selenium dependencies
RUN apk add --no-cache \
    xvfb \
    gdk-pixbuf \
    xvfb-run \
    dbus \
    ttf-freefont \
    chromium \
    chromium-chromedriver

# Copy sources and builded sources
WORKDIR /cli

# Install python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src src

CMD sh -c "python src/main.py runner"
