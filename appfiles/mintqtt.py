import appfiles
from cherrystrap import logger, formatter
import mintapi
from appfiles.mqtt import establish_sensor, update_values, update_attributes
import time
import json
from collections import defaultdict

def mintqtt_vars():

    mintqtt_args = [appfiles.MINT_USERNAME, formatter.decode(appfiles.MINT_PASSWORD)]
    mintqtt_kwargs = {}
    if appfiles.INTUIT_ACCOUNT:
        mintqtt_kwargs['intuit_account'] = appfiles.INTUIT_ACCOUNT
    if appfiles.MFA_METHOD:
        mintqtt_kwargs['mfa_method'] = appfiles.MFA_METHOD
        if appfiles.MFA_METHOD == 'soft-token':
            mintqtt_kwargs['mfa_token'] = formatter.decode(appfiles.MFA_TOKEN)
        else:
            if appfiles.MFA_INPUT_CALLBACK:
                mintqtt_kwargs['mfa_input_callback'] = appfiles.MFA_INPUT_CALLBACK
    else:
        pass
    if appfiles.IMAP_ACCOUNT:
        mintqtt_kwargs['imap_account'] = appfiles.IMAP_ACCOUNT
    if appfiles.IMAP_PASSWORD:
        mintqtt_kwargs['imap_password'] = formatter.decode(appfiles.IMAP_PASSWORD)
    if appfiles.IMAP_SERVER:
        mintqtt_kwargs['imap_server'] = appfiles.IMAP_SERVER
    if appfiles.IMAP_FOLDER != "INBOX":
        mintqtt_kwargs['imap_folder'] = appfiles.IMAP_FOLDER
    if appfiles.SESSION_PATH:
        mintqtt_kwargs['session_path'] = appfiles.SESSION_PATH
    if appfiles.WAIT_FOR_SYNC_TIMEOUT:
        mintqtt_kwargs['wait_for_sync_timeout'] = appfiles.WAIT_FOR_SYNC_TIMEOUT
    if appfiles.DRIVER:
        mintqtt_kwargs['driver'] = appfiles.DRIVER
    
    # must include all booleans
    mintqtt_kwargs['headless'] = appfiles.HEADLESS
    mintqtt_kwargs['wait_for_sync'] = appfiles.WAIT_FOR_SYNC
    mintqtt_kwargs['fail_if_stale'] = appfiles.FAIL_IF_STALE
    mintqtt_kwargs['use_chromedriver_on_path'] = appfiles.USE_CHROMEDRIVER_ON_PATH
    mintqtt_kwargs['quit_driver_on_fail'] = appfiles.QUIT_DRIVER_ON_FAIL

    # also want to pass mqtt info
    mintqtt_kwargs['mqtt_client_id'] = appfiles.MQTT_CLIENT_ID
    mintqtt_kwargs['mqtt_broker_addr'] = appfiles.MQTT_BROKER_ADDR
    mintqtt_kwargs['mqtt_broker_port'] = int(appfiles.MQTT_BROKER_PORT)
    mintqtt_kwargs['mqtt_username'] = appfiles.MQTT_USERNAME
    mintqtt_kwargs['mqtt_password'] = formatter.decode(appfiles.MQTT_PASSWORD)
    mintqtt_kwargs['mqtt_prefix'] = appfiles.MQTT_PREFIX

    return mintqtt_args, mintqtt_kwargs

def fetch_accounts(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	try:
		account_data = mint.get_account_data()
		for item in account_data:
			if item['accountStatus'] == "ACTIVE":
				accounts_sensor_kwargs = mqtt_kwargs
				accounts_sensor_kwargs['attributes'] = True
				accounts_sensor_kwargs['units'] = 'USD'
				accounts_sensor_kwargs['icon'] = 'mdi:currency-usd'
				establish_sensor(item['name'], **accounts_sensor_kwargs)
				if item['type'] == "CreditAccount" or item['type'] == "LoanAccount":
					balance = float(item['currentBalance']) * -1
				else:
					balance = float(item['currentBalance'])
				update_values(item['name'], str(round(balance)), **mqtt_kwargs)
				accounts_attributes_kwargs = mqtt_kwargs
				accounts_attributes_kwargs['attrArray'] = item
				update_attributes(item['name'], **accounts_attributes_kwargs)
	except Exception as e:
		logger.error("Could not publish Account Data to MQTT:" % e)

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_budgets(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	budget_data = mint.get_budget_data()

	combinedArr = defaultdict(dict)

	#===== This Month Only ========

	# begin build of array only for budgets that presently exist (this month)
	for d in budget_data:
		if d['budgetDate'][:-3] == time.strftime("%Y-%m"):
			combinedArr[d['category']['name']].update(d)

	#==============================

	#===== Year to Date ===========

	spentYearToDate = defaultdict(float)
	budgetedYearToDate = defaultdict(float)
	for d in budget_data:
		if d['budgetDate'][:-6] == time.strftime("%Y"):
			spentYearToDate[d['category']['name']] += d['amount']
			budgetedYearToDate[d['category']['name']] += d['budgetAmount']
	spentYearToDateList = [{
		'name': name, 
		'spentYearToDate': round(amount)
		} for name, amount in spentYearToDate.items()]
	budgetedYearToDateList = [{
		'name': name, 
		'budgetedYearToDate': round(budgetAmount)
		} for name, budgetAmount in budgetedYearToDate.items()]

	for l in (spentYearToDateList, budgetedYearToDateList):
		for elem in l:
			combinedArr[elem['name']].update(elem)

	#==============================

	#===== Last Twelve Months =====

	spentPreviousTwelve = defaultdict(float)
	budgetedPreviousTwelve = defaultdict(float)
	for d in budget_data:
		spentPreviousTwelve[d['category']['name']] += d['amount']
		budgetedPreviousTwelve[d['category']['name']] += d['budgetAmount']
	spentPreviousTwelveList = [{
		'name': name, 
		'spentPreviousTwelve': round(amount)
		} for name, amount in spentPreviousTwelve.items()]
	budgetedPreviousTwelveList = [{
		'name': name, 
		'budgetedPreviousTwelve': round(budgetAmount)
		} for name, budgetAmount in budgetedPreviousTwelve.items()]

	for l in (spentPreviousTwelveList, budgetedPreviousTwelveList):
		for elem in l:
			combinedArr[elem['name']].update(elem)

	#==============================

	budgetArr = list(combinedArr.values())

	# remove multi-month budgets if payment is not due this month (note: decided to keep this)
	# budgetArr = [x for x in budgetArr if (x.get('type') != "MultimonthBudget" or x.get('paymentDate')[:-3] == time.strftime("%Y-%m"))]

	# opportunity to display this sensor as monthly, year to date, or past twelve months as configurable setting
	# and/or display sensor as progress against budget in terms of dollars or percentage
	try:
		for item in budgetArr:
			if "type" in item:
				if item['name'] == 'Root':
					friendlyName = "Everything Else"
				else:
					friendlyName = item['name'].replace("&","and")
					# below example is to measure percentage of budget spent year-to-date (may be configurable)
					#budgetPerformance = round((int(item['spentYearToDate']) / int(item['budgetedYearToDate'])) * 100)
					# instead sending raw monthly budget remaining to sensor, at least to start
					budgetPerformance = round(int(item['budgetAmount']) - int(item['amount']))

				budgets_sensor_kwargs = mqtt_kwargs
				budgets_sensor_kwargs['attributes'] = True
				#budgets_sensor_kwargs['units'] = '%'
				budgets_sensor_kwargs['units'] = 'USD'
				budgets_sensor_kwargs['icon'] = 'mdi:plus-minus-box'
				
				establish_sensor(friendlyName, **budgets_sensor_kwargs)
				update_values(friendlyName, str(budgetPerformance), **mqtt_kwargs)
				budgets_attributes_kwargs = mqtt_kwargs
				budgets_attributes_kwargs['attrArray'] = item
				update_attributes(friendlyName, **budgets_attributes_kwargs)
	except Exception as e:
		logger.error("Could not publish Budget Data to MQTT:" % e)

	#==============================

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_net_worth(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	try:
		net_worth = mint.get_net_worth_data()
	except Exception as e:
		logger.error("Could not connect to Mint for Net Worth data:" % e)
	try:
		net_worth_sensor_kwargs = mqtt_kwargs
		net_worth_sensor_kwargs['attributes'] = False
		net_worth_sensor_kwargs['units'] = 'USD'
		net_worth_sensor_kwargs['icon'] = 'mdi:currency-usd'
		establish_sensor('Net Worth', **net_worth_sensor_kwargs)
		update_values('Net Worth', str(round(float(net_worth))), **mqtt_kwargs)
	except Exception as e:
		logger.error("Could not publish Net Worth to MQTT:" % e)

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_credit_score(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	try:
		credit_score = mint.get_credit_score_data()
	except Exception as e:
		logger.error("Could not connect to Mint for Credit Score data:" % e)
	try:
		credit_score_sensor_kwargs = mqtt_kwargs
		credit_score_sensor_kwargs['attributes'] = False
		credit_score_sensor_kwargs['units'] = False
		credit_score_sensor_kwargs['icon'] = 'mdi:clipboard-account-outline'
		establish_sensor('Credit Score', **credit_score_sensor_kwargs)
		update_values('Credit Score', str(int(credit_score)), **mqtt_kwargs)
	except Exception as e:
		logger.error("Could not publish Credit Score to MQTT:" % e)

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_bills(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	logger.info(mint.get_bills())

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_investments(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	logger.info(mint.get_investment_data())

	logger.info("Closing connection with Mint")
	mint.close()

	return

def fetch_transactions(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	try:
		transaction_data = mint.get_transaction_data()
	except Exception as e:
		logger.error("Could not connect to Mint for Transaction data:" % e)

	try:
		transactionArr = {}
		spentToday = 0
		count = 0
		for d in transaction_data:
			if d['date'] == time.strftime("%Y-%m-%d"):
				transactionArr[count] = {
					'merchant': d['description'],
					'amount': float(d['amount']),
					'category': d['category']['name']
					}
				# this gives more information, but most of it is irrelevant clutter...
				#transactionArr[count] = d
				spentToday += float(d['amount'])
				count += 1

		transactions_sensor_kwargs = mqtt_kwargs
		transactions_sensor_kwargs['attributes'] = True
		transactions_sensor_kwargs['units'] = 'USD'
		transactions_sensor_kwargs['icon'] = 'mdi:network-pos'
		establish_sensor("Posted Transactions", **transactions_sensor_kwargs)
		update_values("Posted Transactions", str(round(float(spentToday))), **mqtt_kwargs)
		transactions_attributes_kwargs = mqtt_kwargs
		transactions_attributes_kwargs['attrArray'] = transactionArr
		update_attributes("Posted Transactions", **transactions_attributes_kwargs)
	except Exception as e:
		logger.error("Could not publish Transaction Data to MQTT:" % e)

	logger.info("Closing connection with Mint")
	mint.close()

	return

def initiate_refresh(*args, **kwargs):

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	# Connect to Mint
	logger.info("Opening connection with Mint and gathering data")
	mint = mintapi.Mint(args[0], args[1], **kwargs)

	mint.initiate_account_refresh()

	logger.info("Closing connection with Mint")
	mint.close()

	return

def job_list():
	[mintqtt_args, mintqtt_kwargs] = mintqtt_vars()

	if appfiles.FETCH_NET_WORTH:
		fetch_net_worth(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_CREDIT_SCORE:
		fetch_credit_score(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_ACCOUNTS:
		fetch_accounts(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_BUDGETS:
		fetch_budgets(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_BILLS:
		fetch_bills(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_INVESTMENTS:
		fetch_investments(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.FETCH_TRANSACTIONS:
		fetch_transactions(*mintqtt_args, **mintqtt_kwargs)
	if appfiles.INITIATE_REFRESH:
		initiate_refresh(*mintqtt_args, **mintqtt_kwargs)

	return

def delete_sensors():
	update_values('Net Worth', '')
	update_values('Credit Score', '')

if __name__ == '__main__':
	schedule_mint()
	