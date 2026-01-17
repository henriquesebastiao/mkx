FROM python:3.14-alpine
LABEL mantainer="contato@henriquesebastiao.com"

RUN apk update \
    && apk add --no-cache bash pipx \
    && pipx ensurepath \
    && pipx install mkx

CMD ["bash"]