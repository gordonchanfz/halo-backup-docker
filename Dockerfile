FROM python:3.10

LABEL maintainer="gordonchanfz@ainote.cloudns.biz"

ARG TZ='Asia/Shanghai'
WORKDIR /app
COPY . .

RUN apk update && apk --no-cache add curl

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install -U aligo \
	&& pip install git+https://github.com/foyoux/aligo.git \
	&& pip install --no-cache-dir -r requirements.txt

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=048b95b48b708983effb2e5c935a1ef8483d9e3e

RUN curl -fsSLO "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic



# RUN cron job
CMD ["/usr/local/bin/supercronic", "/app/my-cron"]