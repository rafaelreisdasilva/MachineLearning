
Pontos de melhoria:

- O arquivo "Property-Friends-basic-model" poderia ter um nome mais intuitivo e também de modo a facilitar a digitação
-

Análise Exploratória:

Hipóteses:

Estrutura de arquivos:

Bain[Folder] 
    app[Folder] 
        model[Folder]
            documentation [Folder]
            images[Folder]
            Dataset-analysis-train.ipynb
            modelApiEndPoint.py
            Property-Friends-basic-model.ipynb
    dockerfile
    log_modelApiEndPoint.log
    log.log
    requirements.txt

Como Executar o código?

1 - O primeiro passo é gerar a imagem do docker, para isso, devemos executar o comando abaixo:

 docker build -t prediction-chile .

 Ps: Não esquecer do ponto final.

2 O segundo passo é criar n containeres da imagem criada previamente (prediction-chile), o comando é:

 docker container run -p 80:80  prediction-chile 

Utilizamos a porta 80.

3 - Para acessar a API devemos ir no navegador e digitar 

http://localhost/ ou http://0.0.0.0:80

4- Além da introdução fornecida na rota principal, podemos acessar a documentação da api da FASTAPI

 http://localhost/docs documentation

5- Adicionalmente, e quiser criar o container a partir da imagem en
 docker container run nomedocontainer
 docker container ls -a para listar todos os containers
 docker container ls somente os que estao rodando
docker container rm id ou nomedocontainer para remover o container

6 - No mercado comercial de software logs sao importantes, para isso 



Tratamento de Erros:

Pontos da Api:

Resultados: