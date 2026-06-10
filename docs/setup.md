# Guia de Instalação

## Pré-requisitos

* Conta AWS
* Terraform
* Docker
* Ansible
* Git
* Conta GitHub

## Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd cloud-project
```

## Criar a Infraestrutura

```bash
terraform init
terraform apply
```

## Configurar o Servidor

```bash
ansible-playbook -i inventory.ini install-docker.yml
```

## Construir os Containers

Backend:

```bash
docker build -t backend ./services/backend
```

Worker:

```bash
docker build -t worker ./services/worker
```

## Executar os Serviços

Backend:

```bash
docker run -d --name backend -p 5000:5000 backend
```

Worker:

```bash
docker run -d --name worker worker
```

## Verificar o Funcionamento

Estado do Backend:

```bash
curl http://localhost:5000/api/status
```

Enviar mensagem para a fila:

```bash
curl http://localhost:5000/send
```
