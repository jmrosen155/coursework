# models.py
# peewee
# Another popular one: SQLAlchemy

from peewee import * 

db = SqliteDatabase('weather.db')

class City(Model):
	# Define every single column
	# from the database that we
	# want to talk about
	id = IntegerField(primary_key=True)
	city_name = CharField()
	january = DecimalField(max_digits=5,decimal_places=2)
	april = DecimalField(max_digits=5,decimal_places=2)
	july = DecimalField(max_digits=5,decimal_places=2)
	october = DecimalField(max_digits=5,decimal_places=2)
	ann_precip_in = DecimalField(max_digits=5,decimal_places=2)
	ann_precip_days = IntegerField()
	ann_snow_in = DecimalField(max_digits=5,decimal_places=2)
	latitude = DecimalField(max_digits=9,decimal_places=6)
	longitude = DecimalField(max_digits=9,decimal_places=6)


	class Meta:
		database = db
		db_table = "city_averages"




