### Trabalho 1 INF01017 - Redes Neurais e Sistemas Fuzzy
#### Alunos:
 - Christian Schmitz, 242258
 - Igor Pires Ferreira, 242267 
 - Thor Castilhos Sanchotene, 242261

### 1. Detalhes da Implementação
#### 1.1 Classes
##### 1.1.1 Layer
Classe da camada que contém apenas uma lista de neurônios (Neuron)
##### 1.1.2 Neuron
Classe do neurônio. Possui os seguintes atributos:
* Inputs - Lista de tuplas contendo as entradas do neurônio. O primeiro elemento é o neurônio (da camada anterior) e o segundo é o seu peso associado. 
* ActivationFn - Função de ativação do neurônio. Tem como valor padrão a função sigmóide
* Output - Saída do neurônio 
* TestOutput - Saída do neurônio para verificação numérica
* Error
##### 1.1.3 NeuralNet
Classe da rede neural. É a principal classe do projeto. Possui os seguintes atributos: 
* NumericalEvaluation - booleano que é indica se a avaliação numérica deve ser feita
* LearningRate - Taxa de aprendizagem da rede
* RegularizationRate - Taxa de regularização da rede
* DatasetMatrix - Matriz completa os dados do dataSet. 
* AttributesList - Parte da datasetMatrix que contém somente os atributos
* ExpectedClassList - Parte da datasetMatrix que contém as classes que devem ser previstas
* PerformanceEvaluator - objeto da classe homônima usada para obter as métricas da rede.
#### 1.2 Normalização
Para cada atributo, são buscados dentro do dataset seus respectivos valores de mínimo e máximo, e então o valor do atributo recebe:
` attr = (attr-min) / (max-min)`
Sendo assim, todos os valores ficam no intervalo [0,1]
### 2. Verificação Numérica
- Verifique a presença do **python2.7** em sua máquina. É importante que seja a versão 2.7. Verifique também a versão do **numpy**, que deve ser a **1.11.0** 
- Extraia o conteúdo enviado no moodle;
- Vá até a pasta de testes dentro de onde se encontra o projeto;
- Rode `python NumericalEvaluation.py` ou simplesmente `./NumericalEvaluation.py` (não esqueça de se certificar que o arquivo possua permissão de execução)

Atente para as primeiras duas linhas que estão no início de cada teste.
Esse código irá calcular as derivadas de uma rede com a configuração [3, 1, 2] das duas formas requisitadas, via backpropagation e via Verificação Numérica. Prints na tela identificarão os valores e a similaridade poderá ser identificada.
