# This is an Flask based API made for a vehicle company in ireland 

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import datetime


app = Flask(__name__)

@app.route('/')
#root
def index():
	#render the homepage with the form for input queryid
	return render_template('index.html')

@app.route('/datafetch', methods= ['POST'])
def fetch():
	#render view.html with car suggestions
	#Dataframe operations based on queryid
	 
	df = pd.read_csv("Sample.txt", sep="|",usecols=['f1','f3','f6','f11','f12','f22','f23','f26']) #Reads csv file
	df=df[df.f1 == int(request.form['queryid'])] #fetches queryid from index.html

	if len(df) == 0: #If no entry of the query
		#then
		return redirect(url_for('index')) #directs back to homepage
	
	
	dummy_dayElem=[1,6] #index for cols 'f3' and 'f23' containing datetime
	df=datetime_to_weekday(df,dummy_dayElem) # converts datetime to weekday
	

	df['f27']=df.f11.rmul(df.f12) #highest product of no_bags and no_pass, indicate largest car. If otherwise, please specify definitions of big vs small cars. 
	df=df.sort_values(by='f27', ascending=False) #sorts cars according to sizes

	hrs=hrs_category(df) #categorize duations
	var= booking_category(df.iloc[0,1],df.iloc[0,6],hrs) #purpose of booking business family or other

	df.drop(['f1','f3','f23','f26','f27'], axis=1, inplace=True) #drop unnecessary columns

	df.columns=['price','#_bags','#_passengers','duration'] #rename columns for display
	df=display_table(df,var) #specific rows to be displayed, example for business purpose medium cars.
	
	return render_template('view.html',var = var,tables=[df.to_html(classes='customer',index=False)])


def datetime_to_weekday(df,dummy_dayElem):
	#converts datetime stamps to weekday
	for i, _ in enumerate(dummy_dayElem):
		df[df.columns[dummy_dayElem[i]]]= pd.to_datetime(df[df.columns[dummy_dayElem[i]]]).dt.weekday_name
	return df

def hrs_category(df):
	#categorize durations for switch cases
	if (df.iloc[0,5]<=7):
		hrs=1
	elif (df.iloc[0,5]<=15):
		hrs=2
	else:
		hrs=3
	return hrs 




def booking_category(qday,pday,hrs):
	#switch cases to find the purpose of rent 
	options={'Monday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Tuesday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Wednesday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Thursday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Friday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Saturday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}},
			'Sunday':{'Monday':{1:'business',2:'family',3: 'other'},'Tuesday':{1:'business',2:'family',3: 'other'}
						,'Wednesday':{1:'business',2:'family',3: 'other'},'Thursday':{1:'business',2:'family',3: 'other'}
						,'Friday':{1:'business',2:'family',3: 'other'},'Saturday':{1:'business',2:'family',3: 'other'}
						,'Sunday':{1:'business',2:'family',3: 'other'}}

			}
	return options[qday][pday][hrs]

def display_table(df,var):
	#rows to be displayed
	if var == 'family':
		df=df.iloc[:10] #top ten big cars
	elif var == 'business':
		df=df.iloc[int(len(df)/2)-5:int(len(df)/2)+5]#medium cars
	else:
		df=df.iloc[::int(len(df)/10)] #every alternate car, mixed cars
	return df
	




@app.route('/homer', methods= ['POST'])
#redirect to homepage. Followed this architecture for future modifications.
def homer():
	return redirect(url_for('index'))



# Standard boilerplate to call the main() function.
if __name__ == '__main__':
	app.run(debug = True)		 # Please remove debug = True before publishing.
