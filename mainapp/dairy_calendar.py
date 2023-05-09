from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DayProgress

ru_day_abbr = ["Пн","Вт","Ср","Чт","Пт","Сб", "Вс"]
ru_month_name = ["Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь"] 

class Calendar(HTMLCalendar):
   
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()
     
	# formats a day as a td
	# filter events by day
	def formatday(self, day, weekday):
		if day == 0: return '<td class="%s">&nbsp;</td>' % self.cssclass_noday  # day outside month
		else:
			date = datetime.strptime(f"{self.year}{self.month}{day}", '%Y%m%d').date()
			try:
				data = DayProgress.objects.get(user = self.user, current_date=date)
			except:
				data = ""
			return f'<td class="%s">%s %s</td>' % (self.cssclasses[weekday], day, data)

	# formats a week as a tr 
	def formatweek(self, theweek):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, weekday) # <td class="thu">2</td>
		return f'<tr> {week} </tr>' 

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		#events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n' #creatring a table
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n' #<tr><th colspan="7" class="month">May 2023</th></tr>
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			# week - list of seven-tuples of day numbers and weekday numbers.
			cal += f'{self.formatweek(week)}\n'
		return cal


	#russificated method (instead of default day_abbr)
	def formatweekday(self, day):
		return '<th class="%s">%s</th>' % (self.cssclasses_weekday_head[day], ru_day_abbr[day]) 

	#russificated method (instead of default month_name)
	def formatmonthname(self, theyear, themonth, withyear=True):
		if withyear:
			s = '%s %s' % (ru_month_name[themonth], theyear)
		else:
			s = '%s' % ru_month_name[themonth]
		return '<tr><th colspan="7" class="%s">%s</th></tr>' % (self.cssclass_month_head, s)