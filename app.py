from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  
from create_db import Base, Rooms, Equipment, Clients, Orders
  
app = Flask(__name__)  
  
engine = create_engine('sqlite:///studio.db?check_same_thread=False')  
Base.metadata.bind = engine  
  
DBSession = sessionmaker(bind=engine)  
session = DBSession()  
  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    rooms = session.query(Rooms).all()  
    return render_template('rooms.html', rooms=rooms)

@app.route('/equipment')
def equipment():
    equipment = session.query(Equipment).all()  
    return render_template('equipment.html', equipment=equipment)

@app.route('/rools')
def rools():
    return render_template('rools.html')

def get_available_times(day, duration=1):
    now = datetime.now()
    current_date = datetime.combine(day, datetime.min.time())
    if current_date.date() == now.date():
        # Если бронируется на текущий день, доступное время с текущего часа + 1
        start_hour = now.hour + 1
    else:
        # Если бронируется на другой день, доступное время с 9:00
        start_hour = 9

    # Ограничение до 21:00
    end_hour = 21

    # Получаем все бронирования на указанный день
    orders = session.query(Orders).filter(Orders.day == day).all()

    # Формируем список доступных времен
    available_times = []
    for h in range(start_hour, end_hour):
        time_is_available = True
        for order in orders:
            order_start = order.time.hour
            order_end = order.time.hour + order.duration
            for booked_hour in range(order_start, order_end):
                if h == booked_hour:
                    time_is_available = False
                    break
            if not time_is_available:
                break
        
        if time_is_available:
            time_str = current_date.replace(hour=h, minute=0).strftime('%H:%M')
            available_times.append(time_str)

    return available_times

def is_time_available(day, time, duration):
    end_hour = 21
    if time.hour + duration > end_hour:
        return False

    orders = session.query(Orders).filter(Orders.day == day).all()
    for order in orders:
        order_start = order.time
        order_end = (datetime.combine(day, order.time) + timedelta(hours=order.duration)).time()
        booking_start = time
        booking_end = (datetime.combine(day, time) + timedelta(hours=duration)).time()

        if (booking_start >= order_start and booking_start < order_end) or \
           (booking_end > order_start and booking_end <= order_end):
            return False
    return True


@app.route('/booking', methods=['POST', 'GET'])
def booking():
    if request.method == 'POST': 
        client_name = request.form['client_name']
        client_surname = request.form['client_surname']
        phone_number = request.form['phone_number']
        email = request.form['email']
        room_id = request.form['room']
        equipment_ids = [int(equipment_id) for equipment_id in request.form.getlist('equipment')]
        day = datetime.strptime(request.form['day'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
        duration = int(request.form['duration'])

        # Получение объектов клиента и зала
        client = session.query(Clients).filter_by(client_name=client_name, client_surname=client_surname, phone_number=phone_number, email=email).first()
        room = session.query(Rooms).get(room_id)

        # Проверка доступности времени с учетом длительности и ограничения до 21:00
        if not is_time_available(day, time, duration):
            return "К сожалению, данное время уже занято или превышает разрешенное время бронирования. Пожалуйста, выберите другое время для бронирования"

        # Создание нового клиента    
        client = Clients(client_name=client_name, client_surname=client_surname, phone_number=phone_number, email=email)
        session.add(client)
        session.commit()

        # Создание нового заказа
        new_order = Orders(client_id=client.client_id, room_id=room_id, day=day, time=time, duration=duration)
        if equipment_ids:
            new_order.equipment_id = equipment_ids[0]

        session.add(new_order)
        session.commit()
        return redirect('/')

    now = datetime.now().date()
    rooms = session.query(Rooms).all()
    equipment = session.query(Equipment).all() 
    available_times = get_available_times(now)

    return render_template('booking.html', rooms=rooms, equipment=equipment, now=now, available_times=available_times)

@app.route('/available_times')
def available_times():
    day = datetime.strptime(request.args.get('day'), '%Y-%m-%d').date()
    duration = int(request.args.get('duration', 1))
    times = get_available_times(day, duration)
    return jsonify({'available_times': times})

if __name__ == '__main__':
    app.run(debug=True)
