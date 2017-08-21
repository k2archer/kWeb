
#/* Copyright 2016<Copyright Pwei> */

CC    = gcc
DEBUG_FLAGS   = -g 
LIBS = -lpthread
SRC   = ./src
TMP   = ./tmp
BUILD = ./build
INCLUDE  = ./include

SERVER_BINARY = $(BUILD)/tcpserv
SERVER_OBJECTS = $(TMP)/tcpserv.o
# $(TMP)/weblib.o 

CLIENT__BINARY = $(BUILD)/tcpcli
CLIENT_OBJECTS = $(TMP)/tcpcli.o

BINARY = $(BUILD)/tcpserv $(BUILD)/tcpcli
OBJECTS = $(SERVER_OBJECTS) $(CLIENT_OBJECTS)

all: $(SERVER_BINARY) $(CLIENT__BINARY)
	cp -R -f $(BUILD) /tmp
	-rm $(OBJECTS)

$(TMP)/%.o : src/%.cc
	$(CC) $(DEBUG_FLAGS) -I$(INCLUDE) -c -o $@ $< 

$(SERVER_BINARY) : $(SERVER_OBJECTS)
	$(CC) $< -o $@ $(LIBS) 

$(CLIENT__BINARY) : $(CLIENT_OBJECTS)
	$(CC) $< -o $@

# testing:
# 	$(BUILD)/tcpserv &
# 	@echo 3
# 	@sleep 1
# 	@echo 2
# 	@sleep 1
# 	@echo 1
# 	@sleep 1
# 	$(BUILD)/tcpcli 127.0.0.1

check: 
	-python /bin/cpplint.py $(SRC)/*.cc

.PHONY: clean
clean:
	-rm $(BINARY)
	-rm $(OBJECTS)
	@echo -e "\e[1;32m clean completed \e[0m"

