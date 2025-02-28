# Previsão de Vendas Rossmann

# 0.0 Guideline

Este projeto utiliza dados extraídos e processados a partir dos dados públicos em: [Kaggle: Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales/data)

A API de previsão está hospedada no [Render](https://render.com/)
Além disso, um bot do Telegram está disponível pelo nome de usuário @predicao_warning_bot (RossmannBot).

# 1.0 Problema de Negócio

A Rossmann opera mais de 3.000 farmácias em 7 países da Europa. Como parte de um plano de modernização, o CFO deseja reformar as lojas para melhorar a infraestrutura e o atendimento ao cliente. Para determinar o orçamento de cada loja, os gerentes regionais foram solicitados a fornecer previsões de receita para as próximas 6 semanas. No entanto, a previsão manual tem se mostrado propensa a erros.

**Objetivo:** Automatizar a previsão de receita para os próximos 6 semanas, permitindo que o CFO tome decisões baseadas em dados e avalie quais lojas são elegíveis para reformas.

# 2.0 Premissas de Negócio

1. O CFO deve acessar as previsões de qualquer lugar.
2. O CFO precisa de flexibilidade para analisar cada loja individualmente.
3. Dias em que as lojas estiveram fechadas são excluídos das previsões.
4. Apenas lojas com vendas maiores que zero no histórico são consideradas.

## 2.1 Descrição dos Dados
| Atributo | Descrição |
| -- | -- |
| Store | Identificador único da loja |
| Date | Data da venda |
| DayOfWeek | Dia numérico da semana (1-7) |
| Sales | Receita diária |
| Customers | 	Número de clientes por dia |
| Open | 	Status da loja: 1 = Aberta, 0 = Fechada |
| StateHoliday | Indicador de feriado: a = Público, b = Páscoa, c = Natal, 0 = Nenhum |
| SchoolHoliday | 1 = Fechado por feriado escolar, 0 = Aberto |
| StoreType | Modelo da loja (a, b, c, d) |
| Assortment | Variedade de produtos: a = Básico, b = Extra, c = Estendido |
| CompetitionDistance | 	Distância (metros) até o concorrente mais próximo |
| CompetitionOpenSince | [Mês/Ano] Abertura do concorrente mais próximo |
| Promo | 1 = Promoção ativa, 0 = Nenhuma |
| Promo2 | 1 = Promoção estendida em andamento, 0 = Inativa |
| Promo2Since | [Ano/Semana] Início da promoção estendida |
| PromoInterval | Meses em que promoções estendidas são renovadas (ex.: "Fev, Mai, Ago, Nov") |

# 3.0 Estratégia de Solução
Para a resolução do problema foi utilizado a metodologia CRISP-DM

## 3.1 Fases do CRISP-DM
1. Definição do Problema de Negócio: Identificar stakeholders e objetivos.
2. Compreensão do Negócio: Alinhar expectativas e prototipar soluções.
3. Coleta de Dados: Agregar dados do Kaggle.
4. Limpeza de Dados: Tratar valores ausentes, outliers e inconsistências.
5. Análise Exploratória: Descobrir padrões e criar hipóteses.
6. Modelagem dos Dados: Aplicar transformações estatísticas.
7. Treinamento de Algoritmos: Avaliação de modelos (Holdout, Cross-Validation, Fine-Tuning).
8. Avaliação de Desempenho: Seleção do melhor modelo via MAPE.
9. Deploy da Solução: Publicação da API e um bot no Telegram para acesso do CFO.

## 3.2 Ferramentas Utilizadas
- Python 3.12.4 (Pandas, Scikit-learn, XGBoost, RandomForest)
- Git/GitHub (Controle de versão)
- VSCode/Google Collab (Desenvolvimento)
- Render (Hospedagem da API)
- Telegram API (Integração com bot)

# 4.0 Análise de Dados
Após a limpeza, foram feitas análises estatísticas e testes de hipóteses.

## 4.1 Isights de Negócios

### Lojas deveriam vender mais depois do dia 10 de cada mes.
**VERDADEIRA** As vendas diminuem após o dia 10.
![h1](https://github.com/user-attachments/assets/92ec1a1a-65a2-45d2-b291-068f64df3762)

### Lojas deveriam vender menos aos finais de semana.
**VERDADEIRA** Queda significativa aos domingos.
![h2](https://github.com/user-attachments/assets/490fc8b2-167d-49fd-8873-5acb5a066ffa)

# 5.0 Modelos de Machine Learning
Modelos testados:
  1. Modelo de Média (Baseline)
  2. Regressão Linear
  3. Regressão Lasso
  4. Random Forest Regressor
  5. XGBoost Regressor

# 6.0 Seleção do Modelo

## 6.1 Model Performance (Cross-Validation)



| Model Name | MAE CV | MAPE CV | RMSE CV |
| ----- | --- | ---- | ---- |
|	Linear Regression	|2081.73 +/- 295.63|	0.3 +/- 0.02|	2952.52 +/- 468.37|
|	Lasso|	2116.38 +/- 341.5|	0.29 +/- 0.01|	3057.75 +/- 504.26|
|	Random Forest Regressor|	840.04 +/- 220.0	|0.12 +/- 0.02|	1261.15 +/- 323.09|
|	XGBoost Regressor|	1857.67 +/- 292.27|	0.25 +/- 0.01	|2686.2 +/- 436.3|

## 6.2 Modelo Final: XGBoost Regressor
**Motição:** Melhor custo-benefício na hospedagem no Render.

# 7.0 Resultado de Negócios

## 7.1 Performance do Modelo
- Capturou tendências cíclicas com mínima divergência de erro.
![perf](https://github.com/user-attachments/assets/1df6f1c4-acb3-4078-a0b8-41d4ed8b8916)

## 7.2 Acurácia por Loja
- Maioria das lojas agrupadas perto do 0.1 MAPE
![perf2](https://github.com/user-attachments/assets/57570793-8d07-4e4d-969e-53585db5c5b4)

# 7.3 Impacto Financeiro
|Scenario|	Values|
| ----- | --- | 
|	predictions|	R$285,244,608.00|
|	worst_scenario|	R$284,504,127.24|
|	best_scenario|	R$285,985,138.35|

# 8.0 Deploy em Produção
- **API:** Hospedada no Render
- **Telegram Bot:** @predicao_warning_bot

# 9.0 Conclusão
Este MVP permite com que o CFO planeje reformas de forma estratégica e baseada em dados.






