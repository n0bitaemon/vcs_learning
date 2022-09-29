#include <stdio.h>
#include <time.h>

int main(){
	time_t mytime = time(NULL);
	printf(ctime(&mytime));

	return 0;
}
