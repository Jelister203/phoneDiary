import json
from typing import Dict, List
import re


PAGE_SIZE = 10  # Константа, отвечающая за количество записей на странице.

def tableMaper(array):
	"""Подпрограмма стилизации отображаемых данных в консоли."""
	mas = ['━', '┃', '┏', '┓', '┗', '┛', '┣', '┫', '┳', '┻', '╋']
	masDict={i:mas[i] for i in range(len(mas))}
	lenY = len(array)
	lenX = len(array[0])

	size = 0
	for y in range(lenY):
		for x in range(lenX):
			if len(str(array[y][x])) > size:
				size = len(str(array[y][x]))
	for y in range(lenY):
		for x in range(lenX):
			array[y][x]=str(array[y][x]).center(size)

	head = masDict[2]+((masDict[0]*size)+masDict[8])*(lenX-1)+masDict[0]*size+masDict[3]
	bot = masDict[4]+((masDict[0]*size)+masDict[9])*(lenX-1)+masDict[0]*size+masDict[5]
	mid = masDict[6]+((masDict[0]*size)+masDict[10])*(lenX-1)+masDict[0]*size+masDict[7]
	n = [None]*lenY
	first = False
	for y in range(lenY):
		n[y]=masDict[1]+masDict[1].join(list(map(str, array[y])))+masDict[1]
	print(head)
	print(f"\n{mid}\n".join(n))
	print(bot)


def getData() -> List[Dict]:
	"""Подпрограмма для получения записей из файла."""
	with open('data.txt', 'r') as file:
		data = json.loads(file.read())
	return data


def appendData(data=None, userChoice=None):
	"""Подпрограмма для записи данных в файл."""
	Data = getData()
	if userChoice is None:
		Data.append(data)
	else:
		Data[userChoice] = data
	with open('data.txt', 'w') as file:
		file.write(json.dumps(Data))
	return

def showData(first: int = 0, last: int = PAGE_SIZE, userInput: int = 1):
	"""Подпрограмма для отображения записей."""
	Data = getData()
	data = Data[first:last]
	ar = [
		[
			'№','фамилия',
			'имя','отчество',
			'название организации',
			'телефон (рабочий)',
			'телефон (личный)'
		]
	]
	j = (userInput-1)*10
	for note in data:
		a = note.values()
		j+=1
		ar.append([j,*a])
	print(f'\nСТРАНИЦА {userInput}.')
	tableMaper(ar)
	message = 'Введите номер следующей страницы или выберите действие:\n-1)Выход;\n E)Редактировать\n: '
	userInput: str = input(message)
	if userInput == "-1":
		return
	elif userInput in ['E', 'e', 'edit', 'Edit']:
		new_data, userChoice = editData(data=data)
		if new_data is not None:
			appendData(data=new_data, userChoice=userChoice)
		showData(first=first, last=last)

	else:
		userInput = int(userInput)
		showData(first=PAGE_SIZE*(userInput-1), last=PAGE_SIZE*userInput, userInput=userInput)


def inputData():
	"""Подпрограмма для добавления новых записей."""
	lastName: str = input('Введите фамилию нового пользователя: ')
	firstName: str = input('Введите имя нового пользователя: ')
	fatherName: str = input('Введите отчество нового пользователя: ')
	orgName: str = input('Введите название организации нового пользователя: ')
	jobPhone: str = input('Введите телефон (рабочий) нового пользователя: ')
	ownPhone: str = input('Введите телефон (сотовый) нового пользователя: ')
	data = {
		'lastName':lastName,'firstName':firstName,
		'fatherName':fatherName,'orgName':orgName,
		'jobPhone':jobPhone,'ownPhone':ownPhone
	}
	appendData(data=data)
	return


def editData(data=None):
	"""Подпрограмма для редактирования записей, вызываемая другими подпрограммами."""
	userChoice: int = int(input('Пожалуйста, введите номер записи для изменения (-1 для выхода).\n: '))-1
	if userChoice == -2:
		return
	note = None
	try:
		note = data[userChoice]
	except IndexError:
		print('Введён неверный номер записи. Повторите попытку.')
		editData(data=data)
	ar = [
		[i for i in range(1,7)],
		[
			'фамилия',
			'имя','отчество',
			'название организации',
			'телефон (рабочий)',
			'телефон (личный)'
		], [*note.values()]
	]
	tableMaper(ar)
	userChoice2: int = int(input('Введите номер пункта, который Вы хотите изменить (-1 для выхода).\n: '))
	if userChoice2 == -1:
		return
	numToPartDict = {
		1: 'lastName',
		2: 'firstName',
		3: 'fatherName',
		4: 'company',
		5: 'jobPhone',
		6: 'ownPhone'
	}
	note[numToPartDict[userChoice2]] = str(
		input(f'Введите новое значение:\n{note[numToPartDict[userChoice2]]} -> ')
		or note[numToPartDict[userChoice2]]
		)
	return note, userChoice


def searchData(keyWord=None):
	"""Подпрограмма для поиска записей по ключевым словам."""
	if keyWord is None:
		userInput: str = str(input('Введите ключевое слово.\n: '))
		keyWord = userInput
	serchedData = []
	result = [
		[i for i in range(0,7)],
		[
			'№','фамилия',
			'имя','отчество',
			'название организации',
			'телефон (рабочий)',
			'телефон (личный)'
		]
	]
	j = 0
	data = getData()
	for subData in data:
		j+=1
		for value in subData:
			match = re.search(keyWord, subData[value])
			if match:
				serchedData.append(subData)
				result.append([j,*subData.values()])
				break
	tableMaper(result)
	message = 'Выберите дальнейшее действие:\n1) Редактировать запись;\n2) Выйти\n: '
	userInput: str = input(message)
	if userInput == "1":
		new_data, userChoice = editData(data=data)
		if new_data != None:
			appendData(data=new_data, userChoice=userChoice)
		searchData(keyWord=keyWord)
	else:
		return


def main(message=''):
	"""Главная программа, вызывающая и связывающая все подпрограммы."""
	num: int = int(input(message+'\nВыберите операцию'
		+'(наберите на клавиатуре цифру):'
		+'\n1)Вывести список;\n2)Добавить запись;\n'
		+'3)Поиск записей;\n4)Выйти.\n: '))
	if num == 1:
		showData()
		main('\n')
	elif num == 2:
		inputData()
		main('\nДанные успешно добавлены!\n')
	elif num == 3:
		searchData()
		main('\n')
	elif num == 4:
		pass
	else:
		main('Неверный ввод. Пожалуйста, введите только цифру желаемого действия. Пример ввода:"1"')

main('Здравствуйте!')