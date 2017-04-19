#!/usr/bin/python 2.7.10
# coding: utf-8
#
#				# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#				#									#									
#				#			MESTRADO EM CIENCIAS DA COMPUTACAO		#			
#				#		DISCIPLINA DE COMPUTACAO INSPIRADA PELA NATUREZA	#
#				#			Thiago Giroto Milani	-	01/2017		#																	#                               #                                                                       #
#				# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#Bibliotecas
#
import os
import random 
from random import uniform
#
#
modelo = ['1','1','1','1','0','1','1','0','1','1','1','1'] #Objetivo a ser alcancado
comprimento = 12 #Comprimento do material genetico de cada individuo
num = 10 #Numero de Individuos da populacao
precisao = 3 #Numeros de individuos selecionados para a reproducao
mutation_chance = 0.0001 #A probabilidade de mutacao de um individuo
# 
os.system('touch resultados.txt') #Cria um arquivo para armazenar os resultados.
os.system('touch grafico.txt') #Cria um arquivo para armazenar os resultados para o grafico.
print("\n\nMODELO: %s\n"%''.join(modelo)) #Mostra o modelo na tela
"""
	Armazena o modelo de parada no arquivo 'resultados.txt'
"""
w_resultado = open('resultados.txt','a')
w_resultado.write ("\n\nMODELO: %s\n"%''.join(modelo))
w_resultado.write ('\n')
w_resultado.close()
#
def individuo (min, max):
	"""
		Cria um individuo
	"""
	return [list(bin(int(uniform(0b000000000000+1,0b111111111111+1))))[2:] for i in range (comprimento)]
#
def criaPopulacao():
	"""
		Cria uma nova populacao de individuis
	"""
	return [list(bin(int(uniform(0b000000000000+1,0b111111111111+1)))[2:]) for i in range(num)]
#
def calcularFitness(individuo):
	"""
		Calcuma a aptidao de um individuo em particular
	"""
	fitness = 0
	for i in range(len(individuo)):
		if individuo[i] == modelo[i]:
			fitness += 1
	w_fitness = open('fitness.txt','a')
	w_fitness.write (str(fitness))
	w_fitness.write('\n')
	w_fitness.close()
	return fitness
#
def selection_and_reproduction(population):
	"""
		Pontua todos os elementos da populacao e fica com os melhores, quardando dentro de 'selected'
		Depois mescla o material genetico dos selecionados para criar novos individuos e e uma nova populacao
		(guardando tambem uma copia dos individuos selecionados sem modificar)
		Por fim muta os individuos
	"""
	pontuados = [(calcularFitness(i), i) for i in population] #Calcula a aptidao de cada individuo, e guarda em pares ordenados com o formato (5, [1,2,1,1,4,1,8,9,4,1]) 
	pontuados = [i[1] for i in sorted(pontuados)] #Ordena os pares ordenados e deixa sozinho com o array de valores
	population = pontuados
#
	selected = pontuados[(len(pontuados)-precisao):] #Esta linha seleciona os 'n' individuos do final, onde 'n' e dado por 'precisao'
#
	#Mescla o material ginetico para criar novos individuos
	for i in range(len(population) - precisao):
		ponto = random.randint(1,comprimento-1) #Seleciona um ponto para fazer a fusao
		pai = random.sample(selected, 2) #Seleciona dois pares

		population[i][:ponto] = pai[0][:ponto] #Mescla o material genetico dos pares em cada novo individuo
		population[i][ponto:] = pai[1][ponto:]
	return population #O array 'population' tem agora uma nova populacao de individuos, de retorno
#
def mutation(population):
	"""
		Faz a mutacao dos individuos aleatorio
	"""
	w_grafico = open('grafico.txt','a')
	w_resultado = open('resultados.txt','a')
	novo_valor = 0
	ponto = 0
	for i in range(len(population)-precisao):
		prob = random.random()
		if prob <= mutation_chance: #Cada individuo da populacao (menos os pais) tem uma probabilidade de mutar
			ponto = random.random(0,comprimento-1) #Elege-se um ponto aleatorio
			novo_valor = random.random(0,1) #E um novo valor para este ponto
#
		#E importante lembrar que o novo valor nao e igual ao velho
		while novo_valor == population[i][ponto]:
			novo_valor = random.randint(0,1)
#
		#Aplica-se a poputacao
		population[i][ponto] = novo_valor
		print(" "+(''.join(map(str,population[i])))+"	"+str(prob))
		"""
			Armazena nos arquivos 'resultados.txt' e 'grafico.txt' o individuo e a probabilidade de mutacao.
		"""
		w_grafico.write (" "+(''.join(map(str,population[i])))+"	"+str(prob))
		w_resultado.write (" "+(''.join(map(str,population[i])))+"	"+str(prob))
		w_grafico.write ('\n')
		w_resultado.write ('\n')
	w_grafico.write ('\n')
	w_grafico.close()
	w_resultado.close()
#
	return population
#
population = criaPopulacao() #Inicia uma populacao
print("\nPOPULACAO INICIAL: %s"%[(''.join(map(str,population[i]))) for i in range(len(population))]) #Imprime na tela a populacao inicial
"""
	Armazena a populacao inicial no arquivo 'resultados.txt'
"""
w_resultado = open('resultados.txt','a')
w_resultado.write ("\nPOPULACAO INICIAL: %s"%[(''.join(map(str,population[i]))) for i in range(len(population))])
w_resultado.write ('\n\n')
w_resultado.close()
#
#Evolucao da populacao
for i in range(20):
	print("\nGERACAO "+str(i+1))
	w_grafico = open('grafico.txt','a')
	w_grafico.write("\nGERACAO "+str(i+1)+"\n")
	w_grafico.write ('\n')
	w_grafico.close()
	population = selection_and_reproduction(population)
	population = mutation(population)

print("\nPOPULACAO FINAL: %s"%[(" ".join(map(str,population[i]))) for i in range(len(population))]) #Imprime a populacao mais evoluida
"""
	Armazena a populacao final no arquivo 'resultados.txt'
"""
w_resultado = open('resultados.txt','a')
w_resultado.write ("\nPOPULACAO FINAL: %s"%[(" ".join(map(str,population[i]))) for i in range(len(population))])
w_resultado.write ('\n\n')
w_resultado.close()
print("\n\n")
#
#
#Fim
#
#
