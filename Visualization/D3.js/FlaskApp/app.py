from flask import Flask
from flask import render_template
from models import *

app = Flask(__name__)


@app.route('/')
def index():
	cities_count = City.select().count()
	cities = City.select()
	return render_template('index.html', count=cities_count, cities=cities)


@app.route('/about')
def about():
	return render_template('about.html')


# Mark a parameter in the url by putting < > around it
# and then it will come into the function! like magic
# /schools/school-of-food-and-finance - slug
# /schools/01M292-school-of-food-and-finance
@app.route('/cities/<id>')
def show(id):
	# Aggregate functions
	# SELECT MEDIAN(total_students) FROM schools
	# SELECT MAX(total_students) FROM schools
	# SELECT AVG(total_students) FROM schools
	city = City.get(City.id == id)
	avg_precip = City.select().aggregate(
		fn.Avg(City.ann_precip_in)
	)

	avg_jan = City.select().aggregate(
		fn.Avg(City.january)
	)
	avg_apr = City.select().aggregate(
		fn.Avg(City.april)
	)
	avg_jul = City.select().aggregate(
		fn.Avg(City.july)
	)
	avg_oct = City.select().aggregate(
		fn.Avg(City.october)
	)


	# Get the number of schools with <= students,
	# then divide it by the total number of students
	num_lower_cities = City.select().where(
		City.ann_precip_in <= city.ann_precip_in
	).count()
	city_count_percentile = 100 * num_lower_cities / City.select().count()

	return render_template('show.html', city=city, avg_precip=round(avg_precip, 1), avg_jan=round(avg_jan, 1), avg_apr=round(avg_apr, 1), avg_jul=round(avg_jul, 1), avg_oct=round(avg_oct, 1), city_count_percentile=city_count_percentile)

if __name__ == '__main__':
    app.run(debug=True)