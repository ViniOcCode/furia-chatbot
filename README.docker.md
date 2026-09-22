# Furia ChatBot — Docker Setup

Este projeto roda uma aplicação Flask em Docker.

---

## 🚀 Como construir a imagem

Dentro da raiz do projeto (onde está o Dockerfile), execute:

```bash
docker build -t furia-chatbot:1.0 .
```
___

## 🕹️ Como rodar o container
```bash
docker run --rm -p 8080:5000 furia-chatbot:1.0
```
A porta pode local pode ser qualquer uma! Você escolhe uma para você, ela que vai rodar o localhost. Por exemplo, se você colocar 8080, a aplicação estará rodando na porta 8080, portanto basta colocar isso no navegador:
```bash
http://localhost:8080
```
## Comandos úteis

 - Ver containers rodando:
```bash
docker ps
```
 - Parar um container:
```bash
docker stop <CONTAINER_ID>
```
 - Remover um container:
```bash
docker rm <CONTAINER_ID>
```

 - Remover imagem:
```bash
docker rmi furia-chatbot:1.0
```
