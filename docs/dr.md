# Disaster Recovery (DR)

## Visão Geral

Este projeto implementa uma solução de Disaster Recovery (DR) automatizada utilizando AWS e Terraform.

O ambiente principal está implementado na região **eu-west-1**, enquanto existe um ambiente de standby na região **eu-central-1**. Toda a infraestrutura foi criada através de módulos reutilizáveis do Terraform.

O objetivo desta solução é garantir que, caso a infraestrutura principal fique indisponível, exista um mecanismo automático capaz de ativar o ambiente secundário sem qualquer intervenção manual na consola da AWS.

---

# Arquitetura

## Região Principal (eu-west-1)

- VPC
- EC2 (Servidor da aplicação)
- Amazon RDS PostgreSQL (Multi-AZ)
- Amazon SQS
- AWS Secrets Manager

## Região Standby (eu-central-1)

- VPC
- EC2 Standby
- AWS Secrets Manager

## Componentes de Automação

- AWS Lambda (Controlador de Disaster Recovery)
- Amazon EventBridge (executa a cada 5 minutos)
- GitHub Actions com autenticação OIDC

---

# Estratégia de Disaster Recovery

Foi utilizada uma estratégia **Warm Standby**.

A infraestrutura secundária encontra-se previamente criada, mas a instância EC2 permanece desligada até ser detetada uma falha na infraestrutura principal.

Esta abordagem reduz custos e permite uma recuperação relativamente rápida.

---

# Processo de Failover

O processo ocorre automaticamente da seguinte forma:

1. A instância EC2 principal deixa de estar disponível.
2. O Amazon EventBridge executa automaticamente a função Lambda de 5 em 5 minutos.
3. A Lambda verifica o estado da instância principal.
4. Caso a instância esteja parada, a Lambda inicia automaticamente a instância EC2 da região de standby.
5. O ambiente secundário fica disponível.

Todo este processo ocorre sem qualquer interação manual na consola da AWS.

---

# Rollback

Quando a infraestrutura principal voltar a estar operacional:

1. Desligar a instância EC2 da região de standby.
2. Ligar novamente a instância principal.
3. Confirmar que a aplicação está novamente operacional.
4. Continuar a utilizar a região principal.

---

# Proteção dos Dados

A base de dados utiliza:

- Amazon RDS PostgreSQL
- Configuração Multi-AZ
- Backups automáticos
- AWS Secrets Manager para armazenamento seguro das credenciais

Esta configuração permite aumentar a disponibilidade da base de dados e minimizar a perda de informação.

---

# Objetivos de Recuperação

## RTO (Recovery Time Objective)

O objetivo de recuperação é aproximadamente **5 minutos**.

Este valor depende principalmente da execução automática da Lambda pelo EventBridge e do tempo necessário para iniciar a instância EC2 de standby.

## RPO (Recovery Point Objective)

O objetivo é minimizar a perda de dados.

A utilização do Amazon RDS Multi-AZ e dos backups automáticos permite manter uma elevada disponibilidade da base de dados.

---

# CI/CD

O projeto inclui uma pipeline automatizada através do GitHub Actions que permite:

- Executar Terraform Plan
- Executar Terraform Apply
- Construir e publicar as imagens Docker
- Autenticação na AWS através de OIDC
- Executar um Disaster Recovery Drill através de workflow_dispatch

---

# Teste de Disaster Recovery

Para testar a solução:

1. Executar o workflow **Failover Drill** no GitHub Actions.
2. O workflow desliga automaticamente a instância principal.
3. Aguardar a execução da Lambda.
4. Confirmar que a instância da região de standby foi iniciada automaticamente.
5. Registar o tempo de recuperação obtido.

---

# Conclusão

A solução desenvolvida cumpre os requisitos da Época Especial através da implementação de uma arquitetura multi-região, infraestrutura como código, Disaster Recovery automatizado, autenticação segura com OIDC, gestão segura de segredos com AWS Secrets Manager e uma pipeline CI/CD totalmente automatizada.