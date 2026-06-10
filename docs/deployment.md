# Deployment

## Criação da Infraestrutura

A infraestrutura é criada automaticamente através do Terraform.

```bash
terraform init
terraform apply
```

São criados os seguintes recursos:

* VPC
* Subnet Pública
* Internet Gateway
* Route Table
* Security Group
* Instância EC2
* IAM Role
* AWS SQS

## Configuração do Servidor

A instalação do Docker é realizada automaticamente através do Ansible.

```bash
ansible-playbook -i inventory.ini install-docker.yml
```

## Pipeline CI/CD

O processo de CI/CD é executado através do GitHub Actions.

Etapas:

1. Push para a branch main
2. Construção da imagem Backend
3. Construção da imagem Worker
4. Publicação das imagens no Docker Hub

## Execução dos Containers

Backend:

```bash
docker run -d --name backend -p 5000:5000 IMAGE
```

Worker:

```bash
docker run -d --name worker IMAGE
```

## Fluxo da Aplicação

Utilizador

↓

Backend

↓

AWS SQS

↓

Worker
