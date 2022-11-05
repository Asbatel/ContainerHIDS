#modes of chunking paths
MODE_SO = 'STAT/OPEN'
MODE_EX = 'EXECVE'
MODE_CL = 'CLONE'


#syscalls
OPEN = 'open'
STAT = 'stat'
EXECVE = 'execve'
CLONE = 'clone'

ARGS_COL = 'args'
SYSCALL_COL = 'syscall'

SYSDIG = 'sysdig'
READ = '-r'
LOSS = 'loss'

ANOMALY = 'anomaly'
NORMAL =  'normal'

# event

EVENT_LENGTH = 20
NOISY_SCAP_METADATA = ['container', 'json', 'expecting', 'falcosecurity-libs']


#Intersting Sysdig Fields
COLUMNS = ['timestamp', 'syscall', 'args']


# extension
SCAP_EXTENSION = '.scap'



UTF = 'utf-8'
EMPTY = ''
OUTPUT_FILES_NAMES = ['seen_syscalls', 'seen_args', 'max_freq', 'thresh_list']


#nodes
USN = 'USN'
UAN = 'UAN'

WEIGHT = 'weight'


#terminal messages
EVALUATION_INITIALIZER = 'CHIDS is generating the evaluation results for you. Please wait!!!!!'
EVALUATION_HEADER = '------------ Evaluation Summary ----------'

TRAINING_INITIALIZER = 'CHIDS is generating the required training elements for you. Please wait!!!!!'
TRAINING_HEADERS = '------------ Training Summary ----------'

STYLE = "green bold"