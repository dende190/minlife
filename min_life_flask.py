from flask import Flask, render_template, request, flash, redirect
import datetime

app = Flask(__name__)
app.secret_key= 'some_secret'

@app.route(r'/', methods=['GET'])
def home_page():
	now = datetime.datetime.now()
	return render_template('index.html', now = now)

@app.route(r'/min-life', methods=['GET'])
def min_life():
	now = datetime.datetime.now()
	if request.method == 'GET':
		date = request.args.get('bday').split('-')
		if date == ['']:
			flash(' DATOS ERRONEOS, INGRESE DATOS CORRECTOS POR FAVOR ')
			return render_template('index.html')
		else:
			if int(date[0]) > now.year or int(date[0]) < 1950 or (int(date[0]) == now.year and int(date[1]) >= now.month and int(date[2]) >= now.day) or (int(date[0]) == now.year and int(date[1]) > now.month):
				flash(' DATOS ERRONEOS, INGRESE DATOS CORRECTOS POR FAVOR ')
				return render_template('index.html')

		edad = date_to_minuts(date)
		date_year = int(edad[0])
		date_month = int(edad[1])	
		date_day = int(edad[2])

		minutos = convert_min(edad)

		return render_template('time.html', years_old= date_year, month_old = date_month, day_old= date_day, minutos= minutos[1])

def date_to_minuts(date):
	day_of_month = [1, -2, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
	cont = 0
	cont_month_of_year_old = 0

	### OPERACIONES PARA SACAR LOS DIAS FALTANTES DEL AÑO (MESES CON 31 DIAS Y AÑOS BISIESTOS):
	
	### Todas las operaciones van solo por 30 dias sumarle el dia que falta a los meses que tienen 31 dias 
	### agregarle el dia que falta desde que nacio hasta finalziar ese año
	for i in range( int(date[1]) -1, 12):
		now = datetime.datetime.now()
		cont += day_of_month[i]
	### contador de todos los dias que faltan a lo largo de los años que tiene 
	for i in range(0, 12):
		now = datetime.datetime.now()
		cont_month_of_year_old += day_of_month[i]
	cont += (cont_month_of_year_old * ((now.year - 1) - int(date[0])))
	### Agregarle el dia que falta desde que comenzo el año hasta la fecha actual (sin contar el mes en el que se encuentra)
	for i in range(0, now.month - 1):
		now = datetime.datetime.now()
		cont += day_of_month[i]
	### Operaciones para saber sumar los dias de los años bisiestos
	if int(date[1]) > 2:
		now = datetime.datetime.now()
		n = 1 ### N sera el numero para saber si se toma ese año o no
	else:
		now = datetime.datetime.now()
		n = 0
	for i in range(int(date[0]), now.year + n):
		now = datetime.datetime.now()
		if i % 4 == 0:
			now = datetime.datetime.now()
			### es un año bisiesto
			cont += 1

	###OPERACIONES PARA SACAR AÑO, MESES Y DIAS DE LA PERSONA:	

	### revisar los meses, comparacion de mes_now y mes_birthday
	if int(date[1]) > now.month:
		now = datetime.datetime.now()
		### No ha cumplido años, quitarle un año a la fecha actual
		new_year = now.year - 1
		### restar los años
		years_old = new_year - int(date[0])  ####### AÑOS DE LA PERSONA

		### Revisar los dias, comprar dia_now y dia_birthday
		if int(date[2]) > now.day:
			now = datetime.datetime.now()
			### Restar los dias
			days_old = (30 - int(date[2])) + now.day ####### DIAS DE LA PERSONA
			### No ha cumplido el mes, quitarle un mes a la fecha actual
			new_month = now.month - 1
			month_old = (12 - int(date[1])) + new_month ####### MESES DE LA PERSONA

		else:
			now = datetime.datetime.now()
			### Restar los dias
			days_old = now.day - int(date[2]) ####### DIAS DE LA PERSONA
			## Ya cumplio el mes
			month_old = (12 - int(date[1])) + now.month ####### MESES DE LA PERSONA

	elif int(date[1]) == now.month:
		now = datetime.datetime.now()
		## CUMPLEAÑOS, DIA = 0 MES = 0 AÑO = EDAD
		if int(date[2]) <= now.day:
			now = datetime.datetime.now()
			years_old = now.year - int(date[0]) ####### AÑOS DE LA PERSONA
			days_old = now.day - int(date[2]) ####### DIAS DE LA PERSONA
			month_old = now.month - int(date[1]) ####### MESES DE LA PERSONA
		else:
			now = datetime.datetime.now()
			### No ha cumplido el mes

			### No ha cumplido años, quitarle un año a la fecha actual
			new_year = now.year - 1
			### restar los años
			years_old = new_year - int(date[0]) ####### AÑOS DE LA PERSONA
			### Restar los dias
			days_old = (30 - int(date[2])) + now.day ####### DIAS DE LA PERSONA
			### Restar los meses
			### No ha cumplido el mes, quitarle un mes a la fecha actual
			new_month = now.month - 1
			month_old = (12 - int(date[1])) + new_month ####### MESES DE LA PERSONA
	else:
		now = datetime.datetime.now()
		### Ya cumplio años
		if int(date[2]) <= now.day:
			now = datetime.datetime.now()
			### restar los años
			years_old = now.year - int(date[0]) ####### AÑOS DE LA PERSONA
			### Restar los dias
			days_old = now.day - int(date[2]) ####### DIAS DE LA PERSONA
			### Restar los meses
			month_old = now.month - int(date[1]) ####### MESES DE LA PERSONA
		else:
			now = datetime.datetime.now()
			### No ha cumplido el mes

			### restar los años
			years_old = now.year - int(date[0]) ####### AÑOS DE LA PERSONA		
			### Restar los dias
			days_old = (30 - int(date[2])) + now.day ####### DIAS DE LA PERSONA
			### Restar los meses
			### No ha cumplido el mes, quitarle un mes a la fecha actual
			new_month = now.month - 1
			month_old = new_month - int(date[1])

	return [years_old, month_old, days_old, cont]

def convert_min(edad_persona):
	now = datetime.datetime.now()
	### pasar los años a meses:
	years_to_months = edad_persona[0] * 12
	edad_persona[1] += years_to_months 

	### pasar los meses a dias:
	months_to_days = int(edad_persona[1] * 30.41)  ### 30.41
	### agregar los dias faltantes
	edad_persona[2] += months_to_days + edad_persona[3]
	months_to_days = edad_persona[2] 

	### pasar los dias a horas:
	days_to_hours = edad_persona[2] * 24
	days_to_hours += now.hour
	
	### pasar las horas a minutos:
	hours_to_minuts = days_to_hours * 60
	hours_to_minuts += now.minute

	### Agregar signos de separacion:
	data_list = [hours_to_minuts, days_to_hours, months_to_days, years_to_months]
	result = separacion(data_list)

	return result

def separacion(value):
	now = datetime.datetime.now()
	data_list = [value[0]]
	nuevo_numero = 0
	for i in range(len(value)):
		numero = str(value[i])
		largo = len(numero)
		if largo > 3:
			medida = largo - 3
			if medida <= 3:
				nuevo_numero = numero[0 : medida] + '.' + numero[medida : largo]
			elif medida > 3 and medida <= 6:
				medida2 = medida - 3	
				nuevo_numero = numero[0 : medida2] + '\'' + numero[medida2 : medida] + '.' + numero[medida : largo]
			elif medida > 6 and medida <= 9:
				medida3 = medida2 - 3
				nuevo_numero = numero[0 : medida3] + '.' + numero[medida3 : medida2] + '\'' + numero[medida2 : medida] + '.' + numero[medida : largo]
		else:
			nuevo_numero = numero
		
		data_list.append(nuevo_numero)

	return data_list


if __name__ == '__main__':
	now = datetime.datetime.now()
	app.debug = True
	app.run(port=9001)