from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, Rooms, Equipment, Clients, Orders

engine = create_engine('sqlite:///studio.db') 
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

room_one = Rooms(room_name="Mini", 
                 description="Небольшое светлое пространство для любых видов съемок. В зале белый пол, белые стены, розовая стена с розовыми шторами, бумажные фотофоны. Базовое оборудование: постоянный свет Godox Fl150R, комплект импульсного света Hensel, кольцевая лампа всегда доступны в зале. Площадь: 25 м2",
                 cost=1200)

room_two = Rooms(room_name="White", 
                 description="Просторный зал с большими белыми стенами, циклорамой и панорамными окнами. В зале есть дизайнерская мебель, живые растения и всё необходимое для комфортной съемки. Базовое оборудование: Profoto d1-500/ d2-500 x3, насадки для Profoto, стойки manfrotto, Profoto Air Remote. Площадь: 90 м2",
                 cost=2400)

room_three = Rooms(room_name="Flat", 
                 description="Зал с большим количеством фотозон и огромным выбором реквизита: торшер, свечи, книги, альбомы с репродукциями великих художников, винтажная посуда, бокалы, зеркала. Базовое оборудование: постоянный свет Godox fl1505, комплект импульсного света Hensel, лампа rgb. Площадь: 60 м2.",
                 cost=3000)

equipment_one = Equipment(equipment_name="Проектор",
                          description="Качество изображения до 4K",
                          cost=500)

equipment_two = Equipment(equipment_name="Бумажный фон",
                          description="Имеются фоны в разных цветах: чёрный, белый, оливковый, розовый, красный",
                          cost=300)

equipment_three = Equipment(equipment_name="Дым-машина",
                          description="Генератор дыма и тумана, используемый для создания необычной атмосферы в кадре",
                          cost=500)

equipment_four = Equipment(equipment_name="Киносвет Arri 1000W",
                          description="Постоянный источник света с высокой мощностью для создания атмосферных кадров",
                          cost=500)

equipment_five = Equipment(equipment_name="Godox 200W",
                          description="Постоянный источник света. В комплекте можно выбрать любую насадку: софтбокс, стрипбокс, октобокс, рефлектор",
                          cost=300)
session.add(room_one)
session.add(room_two)
session.add(room_three)

session.add(equipment_one)
session.add(equipment_two)
session.add(equipment_three)
session.add(equipment_four)
session.add(equipment_five)


'''
equipmentToDelete = session.query(Equipment).filter_by(equipment_id=10).one() 
session.delete(equipmentToDelete) 
'''

session.commit()
