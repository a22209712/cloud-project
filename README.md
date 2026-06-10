# Cloud Project

## Descrição

Este projeto demonstra a implementação de uma infraestrutura cloud utilizando AWS, Terraform, Ansible, Docker e GitHub Actions.

O objetivo é automatizar o provisionamento da infraestrutura, a configuração dos servidores, a criação de imagens Docker e a execução de pipelines de Integração e Entrega Contínua (CI/CD).

---

## Tecnologias Utilizadas

- AWS EC2
- AWS VPC
- Terraform
- Ansible
- Docker
- Docker Hub
- GitHub Actions
- Nginx

---

## Arquitetura

Fluxo principal do sistema:

Desenvolvedor  
→ GitHub Repository  
→ GitHub Actions  
→ Docker Hub  
→ AWS EC2  
→ Container Docker  
→ Aplicação Web

Mais detalhes disponíveis em:

- [Arquitetura](docs/architecture.md)

---

## Estrutura do Projeto

```text
cloud-project/
│
├── app/
│   ├── Dockerfile
│   └── index.html
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

- VPC
- Subnet Pública
- Internet Gateway
- Route Table
- Security Group
- Instância EC2

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

### 3. Construir Imagem Docker

O GitHub Actions cria automaticamente a imagem Docker.

### 4. Publicar no Docker Hub

A imagem é enviada automaticamente para o Docker Hub.

### 5. Executar Aplicação

O container Docker é executado na instância EC2 e disponibiliza a aplicação através da porta 80.

---

## Pipeline CI/CD

Sempre que existe um push para a branch principal (`main`):

1. O GitHub Actions é iniciado.
2. A imagem Docker é construída.
3. A imagem Docker é enviada para o Docker Hub.

Workflow utilizado:

```text
.github/workflows/docker.yml
```

---

## Acesso à Aplicação

A aplicação pode ser acedida através do endereço IP público da instância EC2.

Exemplo:

```text
http://<EC2_PUBLIC_IP>
```

---

## Documentação

- [Arquitetura](docs/architecture.md)
- [Configuração](docs/setup.md)
- [Deployment](docs/deployment.md)
- [Segurança](docs/security.md)
- [Limitações](docs/limitations.md)

---

## Autor

Rafael Ramalhete | a22209712