port = 2
opponent_port = 1
debug = False
framerecord = False
address = "127.0.0.1"
dolphin_executable_path = "../Ishiiruka/build/Binaries"
#dolphin_executable_path = "./squashfs-root/usr/bin"
connect_code = ""
log = None

number_of_inputs = 16
number_of_outputs = 54

###### PARAMS ######
learning_rate = 0.0001
num_episodes = 1000
gamma = 1

hidden_layer = 64

replay_mem_size = 50000
batch_size = 32

egreedy = 1
egreedy_final = 0.05
egreedy_decay = 2000

report_interval = 10
score_to_solve = 195

####################