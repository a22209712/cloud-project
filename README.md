# Cloud Project

## Descrição

Este projeto demonstra a implementação de uma solução Cloud na AWS utilizando Infraestrutura como Código (Terraform), Configuração Automatizada (Ansible), Contentorização (Docker) e Integração/Entrega Contínua (GitHub Actions).

O objetivo é automatizar o provisionamento da infraestrutura, a configuração dos servidores, a criação de imagens Docker e a execução de serviços distribuídos através de filas de mensagens.

---

## Tecnologias Utilizadas

* AWS EC2
* AWS VPC
* AWS SQS
* AWS IAM
* Terraform
* Ansible
* Docker
* Docker Hub
* GitHub Actions
* Python Flask

---

## Arquitetura

Fluxo principal do sistema:

Programador

↓

GitHub Repository

↓

GitHub Actions

↓

Docker Hub

↓

AWS EC2

↓

Backend Container

↓

AWS SQS

↓

Worker Container

Mais detalhes disponíveis em:

* [Arquitetura](docs/architecture.md)

---

## Estrutura do Projeto

```text
cloud-project/
│
├── services/
│   ├── backend/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── worker/
│       ├── worker.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── ansible/
│   ├── inventory.ini
│   └── install-docker.yml
│
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── providers.tf
│       ├── outputs.tf
│       └── backend.tf
│
├── docs/
│   ├── architecture.md
│   ├── setup.md
│   ├── deployment.md
│   ├── security.md
│   └── limitations.md
│
└── .github/
    └── workflows/
        └── docker.yml
```

---

## Infraestrutura

A infraestrutura é criada automaticamente através do Terraform e inclui:

* VPC
* Subnet Pública
* Internet Gateway
* Route Table
* Security Group
* Instância EC2
* IAM Role
* AWS SQS Queue

Região AWS utilizada:

```text
eu-west-1
```

---

## Processo de Deployment

### 1. Criar Infraestrutura

```bash
terraform init
terraform apply
```

### 2. Configurar Servidor

```bash
ansible-playbook -i inventory.ini install-docker.yml
```

### 3. Construir Imagens Docker

O GitHub Actions cria automaticamente as imagens Docker do Backend e do Worker.

### 4. Publicar no Docker Hub

As imagens são enviadas automaticamente para o Docker Hub.

### 5. Executar Containers

Os containers Backend e Worker são executados na instância EC2.

### 6. Comunicação Assíncrona

O Backend envia mensagens para a AWS SQS e o Worker consome essas mensagens.

---

## Pipeline CI/CD

Sempre que existe um push para a branch principal (`main`):

1. O GitHub Actions é iniciado.
2. A imagem Docker do Backend é construída.
3. A imagem Docker do Worker é construída.
4. As imagens são enviadas para o Docker Hub.

Workflow utilizado:

```text
.github/workflows/docker.yml
```

---

## Testes

Verificar Backend:

```bash
curl http://localhost:5000/api/status
```

Enviar mensagem para a fila:

```bash
curl http://localhost:5000/send
```

---

## Documentação

* [Arquitetura](docs/architecture.md)
* [Configuração](docs/setup.md)
* [Deployment](docs/deployment.md)
* [Segurança](docs/security.md)
* [Limitações](docs/limitations.md)

---

## Autor

Rafael Ramalhete | a22209712
