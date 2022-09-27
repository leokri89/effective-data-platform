## Utilizando desvio padrão para detectar outlier automaticamente.

O desvio padrão é uma medida que expressa o grau de dispersão de um conjunto de dados. Ou seja, o desvio padrão indica o quanto um conjunto de dados é uniforme. Quanto mais próximo de 0 for o desvio padrão, mais homogêneo são os dados.

Utilizando o desvio padrão podemos definir a sensibilidade que queremos para ser outlier e se queremos que o outlier seja detectado apenas em valores altos (Upper one-tailed test), valores baixos (Lower one-tailed test) ou ambos (two-tailed test).

Primeiro, precisamos definir qual o tipo de teste queremos e a partir da escolha qual será o z score. Por padrão iremos aplicar o two-tailed test para verificar tanto valores muito baixos quanto valores muito altos e o zscore de 1.645 que corresponde a detectar desvios com uma de apenas 5% de ocorrerem em situações aleatórias. Se o teste for one-tailed test o valor seria superior a 1.96 para identificar valores alto demais e menores que -1.96 para identificar valores baixo demais.