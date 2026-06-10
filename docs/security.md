# Segurança

## Gestão de Identidades e Acessos

Foram aplicadas boas práticas de segurança e o princípio do menor privilégio.

### IAM

* IAM Role associada à instância EC2
* Não são utilizadas Access Keys no código
* Permissões da SQS atribuídas através de IAM Policies

### Autenticação

* Acesso por chave SSH
* Sem autenticação por palavra-passe

### Gestão de Segredos

Os dados sensíveis são armazenados através de:

* GitHub Secrets
* Docker Hub Access Tokens

Nenhuma credencial está armazenada no repositório.

## Segurança de Rede

Security Group configurado com:

### Entradas

* Porta 22 (SSH)
* Porta 80 (HTTP)
* Porta 5000 (Backend API)

### Saídas

* Todo o tráfego permitido

## Estado do Terraform

O estado do Terraform é armazenado remotamente em:

* Amazon S3
* DynamoDB para locking

## Boas Práticas Aplicadas

* Infrastructure as Code
* Remote State
* IAM Roles
* GitHub Secrets
* SSH Keys
