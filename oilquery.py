import os
import re
from time import sleep
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Scrapper(object):
	def __init__(self):
		self.url = "https://w.amsoil.com/lookup/auto-and-light-truck/2022/acura/mdx/3-5l-6-cyl-engine-code-j35y5-2/?volume=us-volume"
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
		if not os.path.exists('./record/records.txt'):
			self.record = []
		else:
			self.record = []
			f=open('./record/records.txt')
			for line in f:
				self.record.append(eval(line))
			f.close()

	def run(self):

		year_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[2]/select'))
		year_options = [item.text for item in year_selector.options][1:]
		for year in year_options:
			if len(self.record)>0 and year>self.record[-1][0]:
				continue
			year_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[2]/select'))
			year_selector.options[year_options.index(year)+1].click()
			sleep(3)

			make_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[4]/select'))
			make_options = [item.text for item in make_selector.options][1:]
			for make in sorted(make_options):
				if len(self.record)>0 and year>=self.record[-1][0] and make<self.record[-1][1]:
					continue
				make_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[4]/select'))
				make_selector.options[make_options.index(make)+1].click()
				sleep(3)

				model_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[6]/select'))
				model_options = [item.text for item in model_selector.options][1:]
				for model in sorted(model_options):
					if len(self.record)>0 and year>=self.record[-1][0] and make<=self.record[-1][1] and model<self.record[-1][2]:
						continue
					model_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[6]/select'))
					model_selector.options[model_options.index(model)+1].click()
					sleep(3)

					engine_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[8]/select'))
					engine_options = [item.text for item in engine_selector.options][1:]
					for engine in sorted(engine_options):
						if len(engine)<=3:
							continue
						if len(self.record)>0 and year>=self.record[-1][0] and make<=self.record[-1][1] and model<=self.record[-1][2] and engine<self.record[-1][2]:
							continue
						engine_selector = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/div[8]/select'))
						engine_selector.options[engine_options.index(engine)+1].click()
						sleep(3)

						self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[2]/section/div/form/div/input').click()

						for i in range(0,20):
							try:
								result_title = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/section/h1/span').text.strip()
							except:
								pass
							for item in result_title.split(' '):
								if item not in engine:
									break
							else:
								break
							# print(result_title.split(' '), engine, engine_options)
							sleep(0.9)
						else:
							raise RuntimeError(f'Error: {year} {make} {model} {engine}')

						sleep(1)

						for i in range(0,5):
							try:
								content = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/section/div[5]').text
								if 'Viscosity:' in content and 'Capacity:' in content:
									break
							except:
								pass
							sleep(1)
						else:
							content=''

						comb=(year.strip(), make.strip(), model.strip(), engine.strip())
						s = '%s %s %s %s'%comb
						s = re.sub('[\(\)\\\,\.\;\:\'\"\/\s]','_',s)

						f=open('./record/records.txt','a')
						f.write(str(comb)+'\n')
						f.close()

						f=open(f'./record/{s}.txt','w')
						f.write(content)
						f.close()

						print('Fetched:',comb)

						sleep(3)

if __name__=='__main__':
	while True:
		try:
			a=Scrapper()
			a.run()
		except:
			a.driver.quit()
			sleep(180)



