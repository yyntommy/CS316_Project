from roommatefinder import app

@event.listens_for(House.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(House(name='Avalon', building='Kilgo'))
    db.session.add(House(name='Banham', building='Edens'))
    db.session.commit()

@event.listens_for(Major.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(House(name='Dance', school='Trinity College of Arts and Sciences'))
    db.session.add(House(name='Economics', building='Trinity College of Arts and Sciences'))
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
