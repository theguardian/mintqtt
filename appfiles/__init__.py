from cherrystrap import logger, formatter
from cherrystrap.configCheck import CheckSection, check_setting_int, check_setting_bool, check_setting_str

# In this file you can declare additional variables specific to your app.
# Use cherrystrap/__init__.py as your guide... below is a commented-out
# example:
#CPU_INFO_PATH = None

GIT_USER = 'theguardian'
GIT_REPO = 'mintqtt'
GIT_BRANCH = 'main'

MINT_USERNAME = None
MINT_PASSWORD = None
INTUIT_ACCOUNT = None
MFA_METHOD = 'sms'
MFA_TOKEN = None
MFA_INPUT_CALLBACK = None
HEADLESS = True
IMAP_ACCOUNT = None
IMAP_PASSWORD = None
IMAP_SERVER = None
IMAP_FOLDER = 'INBOX'
SESSION_PATH = '/srv/mintqtt/data/cache'
WAIT_FOR_SYNC = False
WAIT_FOR_SYNC_TIMEOUT = 300
FAIL_IF_STALE = True
USE_CHROMEDRIVER_ON_PATH = True
DRIVER = None
QUIT_DRIVER_ON_FAIL = True

MQTT_CLIENT_ID = None
MQTT_BROKER_ADDR = None
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = None
MQTT_PASSWORD = None
MQTT_PREFIX = None

SCHEDULER_TYPE = 'disabled'
SCHEDULER_FREQUENCY = 0
SCHEDULER_UNITS = None
SCHEDULER_CRON = None
RUN_ON_BOOT = False

FETCH_ACCOUNTS = False
FETCH_BUDGETS = False
FETCH_NET_WORTH = False
FETCH_CREDIT_SCORE = False
FETCH_BILLS = False
FETCH_INVESTMENTS = False
FETCH_TRANSACTIONS = False
INITIATE_REFRESH = False

def injectVarCheck(CFG):

    global GIT_USER, GIT_REPO, GIT_BRANCH, \
    MINT_USERNAME, MINT_PASSWORD, INTUIT_ACCOUNT, MFA_METHOD, MFA_TOKEN, \
    MFA_INPUT_CALLBACK, HEADLESS, IMAP_ACCOUNT, IMAP_PASSWORD, IMAP_SERVER, \
    IMAP_FOLDER, SESSION_PATH, WAIT_FOR_SYNC, WAIT_FOR_SYNC_TIMEOUT, \
    FAIL_IF_STALE, USE_CHROMEDRIVER_ON_PATH, DRIVER, QUIT_DRIVER_ON_FAIL, \
    MQTT_CLIENT_ID, MQTT_BROKER_ADDR, MQTT_BROKER_PORT, MQTT_USERNAME, MQTT_PASSWORD, \
    MQTT_PREFIX, SCHEDULER_TYPE, SCHEDULER_FREQUENCY, SCHEDULER_UNITS, SCHEDULER_CRON, \
    RUN_ON_BOOT, FETCH_ACCOUNTS, FETCH_BUDGETS, FETCH_NET_WORTH, FETCH_CREDIT_SCORE, \
    FETCH_BILLS, FETCH_INVESTMENTS, FETCH_TRANSACTIONS, INITIATE_REFRESH

    CheckSection(CFG, 'source')
    CheckSection(CFG, 'mintapi')
    CheckSection(CFG, 'mqtt')
    CheckSection(CFG, 'scheduler')
    CheckSection(CFG, 'selector')

    GIT_USER = check_setting_str(CFG, 'source', 'gitUser', 'theguardian')
    GIT_REPO = check_setting_str(CFG, 'source', 'gitRepo', 'mintqtt')
    GIT_BRANCH = check_setting_str(CFG, 'source', 'gitBranch', 'main')

    MINT_USERNAME = check_setting_str(CFG, 'mintapi', 'mintUsername', '')
    MINT_PASSWORD = check_setting_str(CFG, 'mintapi', 'mintPassword', '')
    INTUIT_ACCOUNT = check_setting_str(CFG, 'mintapi', 'intuitAccount', '')
    MFA_METHOD = check_setting_str(CFG, 'mintapi', 'mfaMethod', 'sms')
    MFA_TOKEN = check_setting_str(CFG, 'mintapi', 'mfaToken', '')
    MFA_INPUT_CALLBACK = check_setting_str(CFG, 'mintapi', 'mfaInputCallback', '')
    HEADLESS = check_setting_bool(CFG, 'mintapi', 'headless', True)
    IMAP_ACCOUNT = check_setting_str(CFG, 'mintapi', 'imapAccount', '')
    IMAP_PASSWORD = check_setting_str(CFG, 'mintapi', 'imapPassword', '')
    IMAP_SERVER = check_setting_str(CFG, 'mintapi', 'imapServer', '')
    IMAP_FOLDER = check_setting_str(CFG, 'mintapi', 'imapFolder', 'INBOX')
    SESSION_PATH = check_setting_str(CFG, 'mintapi', 'sessionPath', '/srv/mintqtt/data/cache')
    WAIT_FOR_SYNC = check_setting_bool(CFG, 'mintapi', 'waitForSync', False)
    WAIT_FOR_SYNC_TIMEOUT = check_setting_int(CFG, 'mintapi', 'waitForSyncTimeout', 300)
    FAIL_IF_STALE = check_setting_bool(CFG, 'mintapi', 'failIfStale', True)
    USE_CHROMEDRIVER_ON_PATH = check_setting_bool(CFG, 'mintapi', 'useChromedriverOnPath', True)
    DRIVER = check_setting_str(CFG, 'mintapi', 'driver', '')
    QUIT_DRIVER_ON_FAIL = check_setting_bool(CFG, 'mintapi', 'quitDriverOnFail', True)

    MQTT_CLIENT_ID = check_setting_str(CFG, 'mqtt', 'mqttClientId', '')
    MQTT_BROKER_ADDR = check_setting_str(CFG, 'mqtt', 'mqttBrokerAddr', '')
    MQTT_BROKER_PORT = check_setting_int(CFG, 'mqtt', 'mqttBrokerPort', 1883)
    MQTT_USERNAME = check_setting_str(CFG, 'mqtt', 'mqttUsername', '')
    MQTT_PASSWORD = check_setting_str(CFG, 'mqtt', 'mqttPassword', '')
    MQTT_PREFIX = check_setting_str(CFG, 'mqtt', 'mqttPrefix', '')

    SCHEDULER_TYPE = check_setting_str(CFG, 'scheduler', 'schedulerType', 'disabled')
    SCHEDULER_FREQUENCY = check_setting_int(CFG, 'scheduler', 'schedulerFrequency', 0)
    SCHEDULER_UNITS = check_setting_str(CFG, 'scheduler', 'schedulerUnits', 'hours')
    SCHEDULER_CRON = check_setting_str(CFG, 'scheduler', 'schedulerCron', '0 */8 * * *')
    RUN_ON_BOOT = check_setting_bool(CFG, 'scheduler', 'runOnBoot', False)

    FETCH_ACCOUNTS = check_setting_bool(CFG, 'selector', 'fetchAccounts', False)
    FETCH_BUDGETS = check_setting_bool(CFG, 'selector', 'fetchBudgets', False)
    FETCH_NET_WORTH = check_setting_bool(CFG, 'selector', 'fetchNetWorth', False)
    FETCH_CREDIT_SCORE = check_setting_bool(CFG, 'selector', 'fetchCreditScore', False)
    FETCH_BILLS = check_setting_bool(CFG, 'selector', 'fetchBills', False)
    FETCH_INVESTMENTS = check_setting_bool(CFG, 'selector', 'fetchInvestments', False)
    FETCH_TRANSACTIONS = check_setting_bool(CFG, 'selector', 'fetchTransactions', False)
    INITIATE_REFRESH = check_setting_bool(CFG, 'selector', 'initiateRefresh', False)

def injectDbSchema():

#    schema = {}
#    schema['logpaths'] = {} #this is a table name
#    schema['logpaths']['Program'] = 'TEXT' #this is a column name and format
#    schema['logpaths']['LogPath'] = 'TEXT'

    return schema

def injectApiConfigGet():

    injection = {
        "source": {
            "gitBranch": GIT_BRANCH,
            "gitUser": GIT_USER,
            "gitRepo": GIT_REPO
        },
        "mintapi": {
            "mintUsername": MINT_USERNAME,
            "mintPassword": MINT_PASSWORD,
            "intuitAccount": INTUIT_ACCOUNT,
            "mfaMethod": MFA_METHOD,
            "mfaToken": MFA_TOKEN,
            "mfaInputCallback": MFA_INPUT_CALLBACK,
            "headless": HEADLESS,
            "imapAccount": IMAP_ACCOUNT,
            "imapPassword": IMAP_PASSWORD,
            "imapServer": IMAP_SERVER,
            "imapFolder": IMAP_FOLDER,
            "sessionPath": SESSION_PATH,
            "waitForSync": WAIT_FOR_SYNC,
            "waitForSyncTimeout": WAIT_FOR_SYNC_TIMEOUT,
            "failIfStale": FAIL_IF_STALE,
            "useChromedriverOnPath": USE_CHROMEDRIVER_ON_PATH,
            "driver": DRIVER,
            "quitDriverOnFail": QUIT_DRIVER_ON_FAIL
        },
        "mqtt": {
            "mqttClientId": MQTT_CLIENT_ID,
            "mqttBrokerAddr": MQTT_BROKER_ADDR,
            "mqttBrokerPort": MQTT_BROKER_PORT,
            "mqttUsername": MQTT_USERNAME,
            "mqttPassword": MQTT_PASSWORD,
            "mqttPrefix": MQTT_PREFIX
        },
        "scheduler": {
            "schedulerType": SCHEDULER_TYPE,
            "schedulerFrequency": SCHEDULER_FREQUENCY,
            "schedulerUnits": SCHEDULER_UNITS,
            "schedulerCron": SCHEDULER_CRON,
            "runOnBoot": RUN_ON_BOOT
        },
        "selector": {
            "fetchAccounts": FETCH_ACCOUNTS,
            "fetchBudgets": FETCH_BUDGETS,
            "fetchNetWorth": FETCH_NET_WORTH,
            "fetchCreditScore": FETCH_CREDIT_SCORE,
            "fetchBills": FETCH_BILLS,
            "fetchInvestments": FETCH_INVESTMENTS,
            "fetchTransactions": FETCH_TRANSACTIONS,
            "initiateRefresh": INITIATE_REFRESH
        }
    }

    return injection

def injectApiConfigPut(kwargs, errorList):

    global GIT_USER, GIT_REPO, GIT_BRANCH, \
    MINT_USERNAME, MINT_PASSWORD, INTUIT_ACCOUNT, MFA_METHOD, MFA_TOKEN, \
    MFA_INPUT_CALLBACK, HEADLESS, IMAP_ACCOUNT, IMAP_PASSWORD, IMAP_SERVER, \
    IMAP_FOLDER, SESSION_PATH, WAIT_FOR_SYNC, WAIT_FOR_SYNC_TIMEOUT, \
    FAIL_IF_STALE, USE_CHROMEDRIVER_ON_PATH, DRIVER, QUIT_DRIVER_ON_FAIL, \
    MQTT_CLIENT_ID, MQTT_BROKER_ADDR, MQTT_BROKER_PORT, MQTT_USERNAME, MQTT_PASSWORD, \
    MQTT_PREFIX, SCHEDULER_TYPE, SCHEDULER_FREQUENCY, SCHEDULER_UNITS, SCHEDULER_CRON, \
    RUN_ON_BOOT, FETCH_ACCOUNTS, FETCH_BUDGETS, FETCH_NET_WORTH, FETCH_CREDIT_SCORE, \
    FETCH_BILLS, FETCH_INVESTMENTS, FETCH_TRANSACTIONS, INITIATE_REFRESH


    if 'gitUser' in kwargs:
        GIT_USER = kwargs.pop('gitUser', 'theguardian')
    if 'gitRepo' in kwargs:
        GIT_REPO = kwargs.pop('gitRepo', 'mintqtt')
    if 'gitBranch' in kwargs:
        GIT_BRANCH = kwargs.pop('gitBranch', 'main')
    if 'mintUsername' in kwargs:
        MINT_USERNAME = kwargs.pop('mintUsername', '')
    if 'mintPassword' in kwargs:
        mintPassProcess = kwargs.pop('mintPassword', None)
        if mintPassProcess != MINT_PASSWORD and mintPassProcess != "":
            try:
                MINT_PASSWORD = formatter.encode(mintPassProcess)
            except Exception as e:
                logger.error('There was a problem encoding Mint password: %s' % e)
        elif mintPassProcess == "":
            MINT_PASSWORD = ""
    if 'intuitAccount' in kwargs:
        INTUIT_ACCOUNT = kwargs.pop('intuitAccount', '')
    if 'mfaMethod' in kwargs:
        MFA_METHOD = kwargs.pop('mfaMethod', 'sms')
    if 'mfaToken' in kwargs:
        mfaTokenProcess = kwargs.pop('mfaToken', None)
        if mfaTokenProcess != MFA_TOKEN and mfaTokenProcess != "":
            try:
                MFA_TOKEN = formatter.encode(mfaTokenProcess)
            except Exception as e:
                logger.error('There was a problem encoding MFA Token: %s' % e)
        elif mfaTokenProcess == "":
            MFA_TOKEN = ""
    if 'mfaInputCallback' in kwargs:
        MFA_INPUT_CALLBACK = kwargs.pop('mfaInputCallback', '')
    if 'headless' in kwargs:
        HEADLESS = kwargs.pop('headless', True) == 'true'
    elif 'headlessHidden' in kwargs:
        HEADLESS = kwargs.pop('headlessHidden', True) == 'true'
    if 'imapAccount' in kwargs:
        IMAP_ACCOUNT = kwargs.pop('imapAccount', '')
    if 'imapPassword' in kwargs:
        imapPassProcess = kwargs.pop('imapPassword', None)
        if imapPassProcess != IMAP_PASSWORD and imapPassProcess != "":
            try:
                IMAP_PASSWORD = formatter.encode(imapPassProcess)
            except Exception as e:
                logger.error('There was a problem encoding IMAP password: %s' % e)
        elif imapPassProcess == "":
            IMAP_PASSWORD = ""
    if 'imapServer' in kwargs:
        IMAP_SERVER = kwargs.pop('imapServer', '')
    if 'imapFolder' in kwargs:
        IMAP_FOLDER = kwargs.pop('imapFolder', '')
    if 'sessionPath' in kwargs:
        SESSION_PATH = kwargs.pop('sessionPath', '/srv/mintqtt/data/cache')
    if 'waitForSync' in kwargs:
        WAIT_FOR_SYNC = kwargs.pop('waitForSync', False) == 'true'
    elif 'waitForSyncHidden' in kwargs:
        WAIT_FOR_SYNC = kwargs.pop('waitForSyncHidden', False) == 'true'
    if 'waitForSyncTimeout' in kwargs:
        try:
            WAIT_FOR_SYNC_TIMEOUT = int(kwargs.pop('waitForSyncTimeout', 300))
        except:
            WAIT_FOR_SYNC_TIMEOUT = 300
            errorList.append("waitForSyncTimeout must be an integer")
            kwargs.pop('waitForSyncTimeout', 300)
    if 'failIfStale' in kwargs:
        FAIL_IF_STALE = kwargs.pop('failIfStale', True) == 'true'
    elif 'failIfStaleHidden' in kwargs:
        FAIL_IF_STALE = kwargs.pop('failIfStaleHidden', True) == 'true'
    if 'useChromedriverOnPath' in kwargs:
        USE_CHROMEDRIVER_ON_PATH = kwargs.pop('useChromedriverOnPath', True) == 'true'
    elif 'useChromedriverOnPathHidden' in kwargs:
        USE_CHROMEDRIVER_ON_PATH = kwargs.pop('useChromedriverOnPathHidden', True) == 'true'
    if 'driver' in kwargs:
        DRIVER = kwargs.pop('driver', '')
    if 'quitDriverOnFail' in kwargs:
        QUIT_DRIVER_ON_FAIL = kwargs.pop('quitDriverOnFail', True) == 'true'
    elif 'quitDriverOnFailHidden' in kwargs:
        QUIT_DRIVER_ON_FAIL = kwargs.pop('quitDriverOnFailHidden', True) == 'true'

    if 'mqttClientId' in kwargs:
        MQTT_CLIENT_ID = kwargs.pop('mqttClientId', '')
    if 'mqttBrokerAddr' in kwargs:
        MQTT_BROKER_ADDR = kwargs.pop('mqttBrokerAddr', '')
    if 'mqttBrokerPort' in kwargs:
        try:
            MQTT_BROKER_PORT = int(kwargs.pop('mqttBrokerPort', 1883))
        except:
            MQTT_BROKER_PORT = 1883
            errorList.append("mqttBrokerPort must be an integer")
            kwargs.pop('mqttBrokerPort', 1883)
    if 'mqttUsername' in kwargs:
        MQTT_USERNAME = kwargs.pop('mqttUsername', '')
    if 'mqttPassword' in kwargs:
        mqttPassProcess = kwargs.pop('mqttPassword', None)
        if mqttPassProcess != MQTT_PASSWORD and mqttPassProcess != "":
            try:
                MQTT_PASSWORD = formatter.encode(mqttPassProcess)
            except Exception as e:
                logger.error('There was a problem encoding MQTT password: %s' % e)
        elif mqttPassProcess == "":
            MQTT_PASSWORD = ""
    if 'mqttPrefix' in kwargs:
        MQTT_PREFIX = kwargs.pop('mqttPrefix', '')

    if 'schedulerType' in kwargs:
        SCHEDULER_TYPE = kwargs.pop('schedulerType', 'disabled')
    if 'schedulerFrequency' in kwargs:
        try:
            SCHEDULER_FREQUENCY = int(kwargs.pop('schedulerFrequency', 0))
        except:
            SCHEDULER_FREQUENCY = 0
            errorList.append("schedulerFrequency must be an integer")
            kwargs.pop('schedulerFrequency', 0)
    if 'schedulerUnits' in kwargs:
        SCHEDULER_UNITS = kwargs.pop('schedulerUnits', 'hours')
    if 'schedulerCron' in kwargs:
        SCHEDULER_CRON = kwargs.pop('schedulerCron', '0 */8 * * *')
    if 'runOnBoot' in kwargs:
        RUN_ON_BOOT = kwargs.pop('runOnBoot', True) == 'true'
    elif 'runOnBootHidden' in kwargs:
        RUN_ON_BOOT = kwargs.pop('runOnBootHidden', True) == 'true'

    if 'fetchAccounts' in kwargs:
        FETCH_ACCOUNTS = kwargs.pop('fetchAccounts', True) == 'true'
    elif 'fetchAccountsHidden' in kwargs:
        FETCH_ACCOUNTS = kwargs.pop('fetchAccountsHidden', True) == 'true'
    if 'fetchBudgets' in kwargs:
        FETCH_BUDGETS = kwargs.pop('fetchBudgets', True) == 'true'
    elif 'fetchBudgetsHidden' in kwargs:
        FETCH_BUDGETS = kwargs.pop('fetchBudgetsHidden', True) == 'true'
    if 'fetchNetWorth' in kwargs:
        FETCH_NET_WORTH = kwargs.pop('fetchNetWorth', True) == 'true'
    elif 'fetchNetWorthHidden' in kwargs:
        FETCH_NET_WORTH = kwargs.pop('fetchNetWorthHidden', True) == 'true'
    if 'fetchCreditScore' in kwargs:
        FETCH_CREDIT_SCORE = kwargs.pop('fetchCreditScore', True) == 'true'
    elif 'fetchCreditScoreHidden' in kwargs:
        FETCH_CREDIT_SCORE = kwargs.pop('fetchCreditScoreHidden', True) == 'true'
    if 'fetchBills' in kwargs:
        FETCH_BILLS = kwargs.pop('fetchBills', True) == 'true'
    elif 'fetchBillsHidden' in kwargs:
        FETCH_BILLS = kwargs.pop('fetchBillsHidden', True) == 'true'
    if 'fetchInvestments' in kwargs:
        FETCH_INVESTMENTS = kwargs.pop('fetchInvestments', True) == 'true'
    elif 'fetchInvestmentsHidden' in kwargs:
        FETCH_INVESTMENTS = kwargs.pop('fetchInvestmentsHidden', True) == 'true'
    if 'fetchTransactions' in kwargs:
        FETCH_TRANSACTIONS = kwargs.pop('fetchTransactions', True) == 'true'
    elif 'fetchTransactionsHidden' in kwargs:
        FETCH_TRANSACTIONS = kwargs.pop('fetchTransactionsHidden', True) == 'true'
    if 'initiateRefresh' in kwargs:
        INITIATE_REFRESH = kwargs.pop('initiateRefresh', True) == 'true'
    elif 'initiateRefreshHidden' in kwargs:
        INITIATE_REFRESH = kwargs.pop('initiateRefreshHidden', True) == 'true'

    return kwargs, errorList

def injectVarWrite(new_config):

    new_config['source'] = {}
    new_config['source']['gitUser'] = GIT_USER
    new_config['source']['gitRepo'] = GIT_REPO
    new_config['source']['gitBranch'] = GIT_BRANCH

    new_config['mintapi'] = {}
    new_config['mintapi']['mintUsername'] = MINT_USERNAME
    new_config['mintapi']['mintPassword'] = MINT_PASSWORD
    new_config['mintapi']['intuitAccount'] = INTUIT_ACCOUNT
    new_config['mintapi']['mfaMethod'] = MFA_METHOD
    new_config['mintapi']['mfaToken'] = MFA_TOKEN
    new_config['mintapi']['mfaInputCallback'] = MFA_INPUT_CALLBACK
    new_config['mintapi']['headless'] = HEADLESS
    new_config['mintapi']['imapAccount'] = IMAP_ACCOUNT
    new_config['mintapi']['imapPassword'] = IMAP_PASSWORD
    new_config['mintapi']['imapServer'] = IMAP_SERVER
    new_config['mintapi']['imapFolder'] = IMAP_FOLDER
    new_config['mintapi']['sessionPath'] = SESSION_PATH
    new_config['mintapi']['waitForSync'] = WAIT_FOR_SYNC
    new_config['mintapi']['waitForSyncTimeout'] = WAIT_FOR_SYNC_TIMEOUT
    new_config['mintapi']['failIfStale'] = FAIL_IF_STALE
    new_config['mintapi']['useChromedriverOnPath'] = USE_CHROMEDRIVER_ON_PATH
    new_config['mintapi']['driver'] = DRIVER
    new_config['mintapi']['quitDriverOnFail'] = QUIT_DRIVER_ON_FAIL

    new_config['mqtt'] = {}
    new_config['mqtt']['mqttClientId'] = MQTT_CLIENT_ID
    new_config['mqtt']['mqttBrokerAddr'] = MQTT_BROKER_ADDR
    new_config['mqtt']['mqttBrokerPort'] = MQTT_BROKER_PORT
    new_config['mqtt']['mqttUsername'] = MQTT_USERNAME
    new_config['mqtt']['mqttPassword'] = MQTT_PASSWORD
    new_config['mqtt']['mqttPrefix'] = MQTT_PREFIX

    new_config['scheduler'] = {}
    new_config['scheduler']['schedulerType'] = SCHEDULER_TYPE
    new_config['scheduler']['schedulerFrequency'] = SCHEDULER_FREQUENCY
    new_config['scheduler']['schedulerUnits'] = SCHEDULER_UNITS
    new_config['scheduler']['schedulerCron'] = SCHEDULER_CRON
    new_config['scheduler']['runOnBoot'] = RUN_ON_BOOT

    new_config['selector'] = {}
    new_config['selector']['fetchAccounts'] = FETCH_ACCOUNTS
    new_config['selector']['fetchBudgets'] = FETCH_BUDGETS
    new_config['selector']['fetchNetWorth'] = FETCH_NET_WORTH
    new_config['selector']['fetchCreditScore'] = FETCH_CREDIT_SCORE
    new_config['selector']['fetchBills'] = FETCH_BILLS
    new_config['selector']['fetchInvestments'] = FETCH_INVESTMENTS
    new_config['selector']['fetchTransactions'] = FETCH_TRANSACTIONS
    new_config['selector']['initiateRefresh'] = INITIATE_REFRESH

    return new_config
