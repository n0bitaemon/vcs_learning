CFLAGS += -Werror -Wall

sshtrojan1.so: sshtrojan1.c
	gcc $(CFLAGS) -fPIC -shared -Xlinker -x -o $@ $< -lcurl

