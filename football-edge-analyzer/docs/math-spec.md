# Especificação Matemática

## Probabilidade implícita

```text
p_implicita = 1 / odd
```

## Odd justa

```text
odd_justa = 1 / p_modelo
```

## Valor esperado

```text
EV = (p_modelo * odd_oferecida) - 1
```

## Edge percentual

```text
edge = ((odd_oferecida / odd_justa) - 1) * 100
```

## Remoção de margem em 1X2

```text
p_casa_bruta = 1 / odd_casa
p_empate_bruta = 1 / odd_empate
p_fora_bruta = 1 / odd_fora

overround = p_casa_bruta + p_empate_bruta + p_fora_bruta

p_casa_sem_margem = p_casa_bruta / overround
p_empate_sem_margem = p_empate_bruta / overround
p_fora_sem_margem = p_fora_bruta / overround
```

## Exemplo

```text
Probabilidade estimada: 57%
Odd oferecida: 2.22
Odd justa: 1 / 0.57 = 1.75
EV: (0.57 * 2.22) - 1 = 26.54%
```
